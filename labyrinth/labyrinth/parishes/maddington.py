from ..parish import Parish
from sqlalchemy.sql.functions import func


class Maddington(Parish):
    """
    The Parish of Maddington consists of the localities
    of Maddington and Orange Grove, within the City of
    Gosnells.
    """

    problems = ""

    def geom(self):
        return self.locality_union("Maddington", "Orange Grove")
