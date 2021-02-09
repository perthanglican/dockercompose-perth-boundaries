from ..parish import Parish
from sqlalchemy.sql.functions import func


class Kalamunda(Parish):
    """
    The Parish of Kalamunda consists of the localities of
    Gooseberry Hill and Kalamunda, within the boundary of
    the Shire of Kalamunda
    """

    problems = ""

    def geom(self):
        return self.locality_union("Gooseberry Hill", "Kalamunda")
