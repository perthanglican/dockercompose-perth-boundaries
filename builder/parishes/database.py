
from geoalchemy2 import Geometry, Geography  # noqa
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base


class DatabaseAccess:
    def __init__(self):
        self.engine = self.make_engine()
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


db = DatabaseAccess()
