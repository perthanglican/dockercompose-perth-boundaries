
import json
from .database import db
from sqlalchemy.sql.functions import func
from sqlalchemy.orm.exc import NoResultFound
from traceback import print_stack


class RoadPath:
    def __init__(self, *network_elements):
        self.coords = self.resolve(network_elements)

    def resolve(self, network_elements):
        """
        network_elements should be in consecutive order. jumps between non-contiguous
        elements will result in an interpolated join in the resulting line
        """
        session = db.session()
        try:
            q = session.query(
                func.ST_AsGeoJSON(
                    func.ST_Transform(
                        func.ST_Multi(func.ST_LineMerge(func.ST_Union(db.RoadNetwork.geom))),
                        3857))).filter(
                            db.RoadNetwork.network_element.in_(network_elements))
            cut = json.loads(q.one()[0])
        finally:
            session.close()

        joined = []
        for line in cut['coordinates']:
            joined += line
        return joined


class Cut:
    def __init__(self, description, *paths):
        self.cut = self.resolve(description, paths)

    def resolve(self, description, paths):
        obj = {
            'crs': {'type': 'name', 'properties': {'name': 'EPSG:3857'}},
            'type': 'MultiLineString',
            'coordinates': [t.coords for t in paths]
        }
        session = db.session()
        try:
            q = session.query(
                func.ST_GeomFromGeoJSON(json.dumps(obj)))
            # log for debugging purposes
            session.add(db.Cut(
                description=description,
                geom=func.ST_Transform(q, 4326)))
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
            return self.session.query(db.Localities.geom).filter(db.Localities.name == name.upper()).one()[0]
        except NoResultFound:
            raise Exception("No such locality: {}".format(name))

    def locality_union(self, *args):
        res = func.ST_Union(self.get_locality_by_name(args[0]), self.get_locality_by_name(args[1]))
        for locality in args[1:]:
            res = func.ST_Union(res, self.get_locality_by_name(locality))
        return res

    def cut_locality(self, name, *cuts):
        query = self.session.query(db.Localities.geom).filter(db.Localities.name == name.upper())
        for cut, n in cuts:
            query = func.ST_GeometryN(func.ST_Split(func.ST_Snap(query, cut.cut, 1), cut.cut), n)
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
            problems=getattr(self, 'problems', ''))
        self.session.add(res)
        self.session.commit()
        area = self.session.query(func.ST_Area(db.Result.geom)).filter(db.Result.code == self.get_code())[0][0]
        if area is None or area == 0:
            print("generation failed, empty geometry: {}".format(self.get_code()))
