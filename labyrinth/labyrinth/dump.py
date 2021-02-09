from .database import Result
from sqlalchemy.sql.functions import func


def to_json(db):
    session = db.session()

    def geom_to_geojson(geom):
        return session.query(func.ST_ASGeoJSON(geom)).one()

    def make_parish(p):
        parish = {
            "code": p.code,
            "name": p.name,
            "definition": p.definition,
            "problems": p.problems,
            "geom": geom_to_geojson(p.geom),
        }
        return parish

    parishes = {}
    for result in session.query(Result).all():
        parishes[result.name] = make_parish(result)

    return parishes
