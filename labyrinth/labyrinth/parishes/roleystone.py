from ..parish import Parish
from sqlalchemy.sql.functions import func


class Roleystone(Parish):
    """
    The Parish of Roleystone consists of the localities
    of Roleystone, Karragullen and Illawara, as defined
    by the postal district boundaries (1987) within the
    Town of Armadale
    """

    problems = "refers to obsolete boundaries, Illawara is now Ashendon"

    def geom(self):
        return self.locality_union("Roleystone", "Karragullen", "Ashendon")
