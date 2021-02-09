import math
import json
from sqlalchemy.sql.functions import func


class GeoJSONPath:
    cache_key = "__xx_cache"

    def crs(self, db):
        return self.get_path(db)["crs"]["properties"]["name"]

    def get_path(self, db):
        if not hasattr(self, self.cache_key):
            setattr(self, self.cache_key, self._get_path(db))
        return getattr(self, self.cache_key)


class RoadPath(GeoJSONPath):
    def __init__(self, *network_elements):
        self._network_elements = network_elements

    def _get_path(self, db):
        return self.resolve(db, self._network_elements)

    def resolve(self, db, network_elements):
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
        self._coords = coords

    def _get_path(self, db):
        gj = json.dumps(
            {
                "crs": {"type": "name", "properties": {"name": "EPSG:4326"}},
                "type": "LineString",
                "coordinates": self._coords,
            }
        )
        session = db.session()
        try:
            return json.loads(
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
        self._paths = paths

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

    def _get_path(self, db):
        strands = []

        def add(path):
            ls = path["coordinates"]
            assert type(ls) is list
            strands.append(ls)

        def add_multi(multipath):
            for ls in multipath["coordinates"]:
                assert type(ls) is list
                strands.append(ls)

        for path in (t.get_path(db) for t in self._paths):
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
        crses = list(set(t.crs(db) for t in self._paths))
        assert len(crses) == 1
        return {
            "crs": {"type": "name", "properties": {"name": crses[0]}},
            "type": "LineString",
            "coordinates": coords,
        }


class Cut:
    def __init__(self, description, *paths):
        self._description = description
        self._paths = paths

    def get_cut(self, db):
        f = func.ST_Multi(
            func.ST_GeomFromGeoJSON(json.dumps(self._paths[0].get_path(db)))
        )
        for p in self._paths[1:]:
            f = func.ST_Union(f, func.ST_GeomFromGeoJSON(json.dumps(p.get_path(db))))

        session = db.session()
        try:
            q = session.query(f)
            # log for debugging purposes
            session.add(
                db.Cut(description=self._description, geom=func.ST_Transform(q, 4326))
            )
            session.commit()
            return q.one()[0]
        finally:
            session.close()

