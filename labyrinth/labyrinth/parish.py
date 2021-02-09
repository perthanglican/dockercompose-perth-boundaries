import math
import json
from .database import db
from sqlalchemy.sql.functions import func
from sqlalchemy.orm.exc import NoResultFound
from .util import make_logger


make_logger(__name__)


class GeoJSONPath:
    def crs(self):
        return self.path["crs"]["properties"]["name"]


class RoadPath(GeoJSONPath):
    def __init__(self, *network_elements):
        self.path = self.resolve(network_elements)

    def resolve(self, network_elements):
        """
        network_elements should be in consecutive order. jumps between non-contiguous
        elements will result in an interpolated join in the resulting line
        """
        session = db.session()
        try:
            q = session.query(
                func.ST_AsGeoJSON(func.ST_Multi(func.ST_Union(db.RoadNetwork.geom)))
            ).filter(db.RoadNetwork.network_element.in_(network_elements))
            cut = q.one()[0]
        finally:
            session.close()
        return json.loads(cut)


class LatLngPath(GeoJSONPath):
    def __init__(self, *coords):
        gj = json.dumps(
            {
                "crs": {"type": "name", "properties": {"name": "EPSG:4326"}},
                "type": "LineString",
                "coordinates": coords,
            }
        )
        session = db.session()
        try:
            self.path = json.loads(
                session.query(
                    func.ST_AsGeoJSON(
                        func.ST_Transform(
                            func.ST_Multi(func.ST_GeomFromGeoJSON(gj)), 3857
                        )
                    )
                ).one()[0]
            )
        finally:
            session.close()


class Suture(GeoJSONPath):
    def __init__(self, *paths):
        self.path = self.resolve(paths)

    def suture(self, strands):
        def d(p1, p2):
            x1, y1 = p1
            x2, y2 = p2
            return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        def join(l1, l2):
            if l1[-1] == l2[0]:
                return l1[:-1] + l2
            return l1 + l2

        # pick an arbitrary initial path
        result = strands[0]
        candidates = strands[1:]
        while candidates:
            distances = []
            for candidate in candidates:
                distances.append((d(result[-1], candidate[0]), candidate, iter, iter))
                distances.append(
                    (d(result[-1], candidate[-1]), candidate, iter, reversed)
                )
                distances.append(
                    (d(result[0], candidate[0]), candidate, reversed, iter)
                )
                distances.append(
                    (d(result[0], candidate[-1]), candidate, reversed, reversed)
                )
            distances.sort(key=lambda x: x[0])
            _, candidate, res_iter, cand_iter = distances[0]
            candidates.remove(candidate)
            result = join(list(res_iter(result)), list(cand_iter(candidate)))
        return result

    def resolve(self, paths):
        strands = []

        def add(path):
            ls = path["coordinates"]
            assert type(ls) is list
            strands.append(ls)

        def add_multi(multipath):
            for ls in multipath["coordinates"]:
                assert type(ls) is list
                strands.append(ls)

        for path in (t.path for t in paths):
            if path["type"] == "MultiLineString":
                add_multi(path)
            elif path["type"] == "LineString":
                add(path)
            else:
                raise Exception(
                    "Attempt to suture unknown object: {}".format(path.type)
                )

        coords = self.suture(strands)
        if coords is None:
            return None
        crses = list(set(t.crs() for t in paths))
        assert len(crses) == 1
        return {
            "crs": {"type": "name", "properties": {"name": crses[0]}},
            "type": "LineString",
            "coordinates": coords,
        }


class Cut:
    def __init__(self, description, *paths):
        self.cut = self.resolve(description, paths)

    def resolve(self, description, paths):
        f = func.ST_Multi(func.ST_GeomFromGeoJSON(json.dumps(paths[0].path)))
        for p in paths[1:]:
            f = func.ST_Union(f, func.ST_GeomFromGeoJSON(json.dumps(p.path)))

        session = db.session()
        try:
            q = session.query(f)
            # log for debugging purposes
            session.add(
                db.Cut(description=description, geom=func.ST_Transform(q, 4326))
            )
            session.commit()
            return q.one()[0]
        finally:
            session.close()


class Parish:
    name = None
    code = None

    def __init__(self):
        self.session = db.session()

    @classmethod
    def get_code(cls):
        return cls.code or cls.__name__

    def get_locality_by_name(self, name):
        try:
            return (
                self.session.query(db.Localities.geom)
                .filter(db.Localities.name == name.upper())
                .one()[0]
            )
        except NoResultFound:
            raise Exception("No such locality: {}".format(name))

    def locality_union(self, *args):
        res = func.ST_Union(
            self.get_locality_by_name(args[0]), self.get_locality_by_name(args[1])
        )
        for locality in args[1:]:
            res = func.ST_Union(res, self.get_locality_by_name(locality))
        return res

    def cut_locality(self, name, *cuts):
        query = self.session.query(db.Localities.geom).filter(
            db.Localities.name == name.upper()
        )
        for cut, n in cuts:
            query = func.ST_GeometryN(
                func.ST_Split(func.ST_Snap(query, cut.cut, 1), cut.cut), n
            )
        try:
            return query
        except NoResultFound:
            raise Exception("Cutting non-existent locality: {}".format(name))

    def geom(self):
        """
        calculates the geometry of the parish (abstract)
        """
        return None

    def generate(self):
        res = db.Result(
            code=self.get_code(),
            name=self.name or "Anglican Parish of {}".format(self.get_code()),
            definition=self.__doc__,
            geom=func.ST_Transform(func.ST_Multi(self.geom()), 4326),
            problems=getattr(self, "problems", ""),
        )
        self.session.add(res)
        self.session.commit()
        area = self.session.query(func.ST_Area(db.Result.geom)).filter(
            db.Result.code == self.get_code()
        )[0][0]
        if area is None or area == 0:
            print("generation failed, empty geometry: {}".format(self.get_code()))
