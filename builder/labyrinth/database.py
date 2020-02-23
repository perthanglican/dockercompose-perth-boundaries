
from geoalchemy2 import Geometry, Geography  # noqa
from sqlalchemy import create_engine, MetaData, Column, String, Integer
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DecBase = declarative_base()
Session = sessionmaker()


class DatabaseAccess:
    def __init__(self):
        self.engine = self.make_engine()
        DecBase.metadata.create_all(self.engine)
        self.reflect()

    def make_engine(self):
        return create_engine("postgres://postgres:postgres@db/perth")

    def reflect(self):
        metadata = MetaData()
        metadata.reflect(self.engine, only=[
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

    def session(self):
        return Session(bind=self.engine)


class Result(DecBase):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)
    name = Column(String, unique=True)
    definition = Column(String)
    problems = Column(String)
    geom = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326))


db = DatabaseAccess()
