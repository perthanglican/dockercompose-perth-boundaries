import math
import json
from sqlalchemy.sql.functions import func
from sqlalchemy.orm.exc import NoResultFound
from .util import make_logger


make_logger(__name__)


class Parish:
    name = None
    code = None

    def __init__(self, db):
        self._db = db
        self.session = self._db.session()

    @classmethod
    def get_code(cls):
        return cls.code or cls.__name__

    def get_locality_by_name(self, name):
        try:
            return (
                self.session.query(self._db.Localities.geom)
                .filter(self._db.Localities.name == name.upper())
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
        query = self.session.query(self._db.Localities.geom).filter(
            self._db.Localities.name == name.upper()
        )
        for cut, n in cuts:
            query = func.ST_GeometryN(
                func.ST_Split(
                    func.ST_Snap(query, cut.get_cut(self._db), 1), cut.get_cut(self._db)
                ),
                n,
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
        res = self._db.Result(
            code=self.get_code(),
            name=self.name or "Anglican Parish of {}".format(self.get_code()),
            definition=self.__doc__,
            geom=func.ST_Transform(func.ST_Multi(self.geom()), 4326),
            problems=getattr(self, "problems", ""),
        )
        self.session.add(res)
        self.session.commit()
        area = self.session.query(func.ST_Area(self._db.Result.geom)).filter(
            self._db.Result.code == self.get_code()
        )[0][0]
        if area is None or area == 0:
            print("generation failed, empty geometry: {}".format(self.get_code()))
