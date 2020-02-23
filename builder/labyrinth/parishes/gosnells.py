
from ..parish import Parish
from sqlalchemy.sql.functions import func


class Gosnells(Parish):
    """
    The Parish of Gosnells to serve the localities of Gosnells and MArtine, with boundaries as follows:

    Northern: Gosnells Road.
    Western: Southern Revier.
    Eastern: Coinciding with the Eastern boundary of the City of Gosnells.
    Southern: Coincinding with the Southern boundary of the City of Gosnells.
    """
    problems = "Description may not match current localities"

    def geom(self):
        return self.locality_union('Gosnells', 'Martin')
