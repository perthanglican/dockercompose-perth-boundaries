
from ..parish import Parish
from sqlalchemy.sql.functions import func
from .bayswater import Bayswater


class Bassendean(Parish):
    """
    The Parish of Bassendean consists of the localities of Bassendean,
    Ashfield, and that portion of the locality of Bayswater lying to the
    east of the line of Gray Street from Walter Road to Collier Road, and
    then the line of Jackson Street to Wicks Street, along Wicks Street to
    Vincent Street and along Vincent Street to the railway line.
    """
    problems = "Locality of Bayswater boundary relies on non-existant roads"

    def geom(self):
        def cut_bayswater():
            return self.cut_locality('BAYSWATER', (Bayswater.BAYSWATER_GREY_ST, 2))

        return func.ST_Union(
            self.locality_union('Bassendean', 'Ashfield'),
            cut_bayswater())
