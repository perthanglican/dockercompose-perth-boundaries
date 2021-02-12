from .database import Result
from sqlalchemy.sql.functions import func


def to_json(db):
    session = db.session()

    def geom_to_geojson(geom):
        return session.query(func.ST_ASGeoJSON(geom)).one()[0]

    def make_parish(p):
        def to_lines(s):
            return [t.strip() for t in s.split("\n")]

        parish = {
            "code": p.code,
            "name": p.name,
            "definition": to_lines(p.definition),
            "problems": to_lines(p.problems),
            "geom": geom_to_geojson(p.geom),
        }
        return parish

    parishes = []
    for result in session.query(Result).all():
        parishes.append(make_parish(result))
    parishes.sort(key=lambda p: p["code"])

    return {"parishes": parishes}
