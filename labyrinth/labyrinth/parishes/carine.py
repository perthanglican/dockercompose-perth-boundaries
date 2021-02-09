from ..parish import Parish
from sqlalchemy.sql.functions import func


class CarineDuncraig(Parish):
    """
    The Parish of Carine/Duncraig consists of the localities
    of Duncraig and Carine.
    """

    code = "Carine/Duncraig"
    name = "Anglican Parish of Carine/Duncraig"
    problems = ""

    def geom(self):
        return self.locality_union("Carine", "Duncraig")
