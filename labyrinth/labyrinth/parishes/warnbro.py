from ..parish import Parish
from sqlalchemy.sql.functions import func


class Warnbro(Parish):
    """
    The Parish of Warnbro...
    """

    problems = "no description"

    def geom(self):
        return self.get_locality_by_name("Warnbro")
