
from geoalchemy2 import Geometry, Geography  # noqa
from sqlalchemy import create_engine, MetaData, Column, String, Integer
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DecBase = declarative_base()
Session = sessionmaker()


class DatabaseAccess:
    def __init__(self):
        # lazy so that it can be run from the tests
        self._engine = None

    def connect(self):
        if self._engine is not None:
            return
        self._engine = self.make_engine()
        DecBase.metadata.create_all(self._engine)
        self.reflect()
        self.cleanup()

    def cleanup(self):
        session = self.session()
        session.query(self.Result).delete()
        session.query(self.Cut).delete()
        session.commit()

    def make_engine(self):
        return create_engine("postgres://postgres:postgres@db/perth")

    def reflect(self):
        metadata = MetaData()
        metadata.reflect(self._engine, only=[
            'intersections',
            'localities',
            'lgas',
            'road_network'])
        Base = automap_base(metadata=metadata)
        Base.prepare()
        self.Intersections = Base.classes.intersections
        self.Localities = Base.classes.localities
        self.LGAs = Base.classes.lgas
        self.RoadNetwork = Base.classes.road_network
        self.Result = Result
        self.Cut = Cut

    def session(self):
        self.connect()
        return Session(bind=self._engine)


class Result(DecBase):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)
    name = Column(String, unique=True)
    definition = Column(String, unique=True)
    problems = Column(String)
    geom = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326))


class Cut(DecBase):
    __tablename__ = 'debug_cuts'
    id = Column(Integer, primary_key=True)
    geom = Column(Geometry(geometry_type='MULTILINESTRING', srid=4326))
    description = Column(String)


db = DatabaseAccess()
