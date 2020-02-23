
import json
from .database import db
from sqlalchemy.sql.functions import func
from sqlalchemy.orm.exc import NoResultFound

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

    def cut_locality(self, name, n, defn):
        cut = self.make_road_slice(defn)
        try:
            return self.session.query(
                func.ST_GeometryN(
                    func.ST_Split(db.Localities.geom, cut),
                    n)).filter(db.Localities.name == name.upper()).one()[0]
        except NoResultFound:
            raise Exception("Cutting non-existent locality: {}".format(name))

    def make_road_slice(self, roads):
        def project(p1, p2):
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            dx_dy = dx / dy
            return [p1[0] + (5 * dx), p1[1] + (5 * dx / dx_dy)]

        cut = json.loads(
            self.session.query(
                func.ST_AsGeoJSON(
                    func.ST_Transform(
                        func.ST_Multi(
                            func.ST_LineMerge(
                                func.ST_Union(db.RoadNetwork.geom))),
                        3857)))
            .filter(db.RoadNetwork.objectid.in_(roads)).one()[0])
        joined = []
        for line in cut['coordinates']:
            joined += line
        joined = [project(joined[1], joined[0])] + joined + [project(joined[-4], joined[-1])]
        # project out to make sure we can slice polygon
        cut['type'] = 'LineString'
        cut['coordinates'] = joined

        return self.session.query(
            func.ST_GeomFromGeoJSON(json.dumps(cut))).one()[0]

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
