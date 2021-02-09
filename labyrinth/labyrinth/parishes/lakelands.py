from ..parish import Parish
from sqlalchemy.sql.functions import func


class Lakelands(Parish):
    """
    The Parish of Lakelands to serve the localities of:-

    South Lake (Banjup)
    Bibra Lake (Success)
    Yangebup (Wattleup)
    Jandakot (Munster east of Stock Road)
    """

    problems = "Localities have changed, description needs update"

    def geom(self):
        return self.locality_union(
            "Banjup",
            "Bibra Lake",
            "Success",
            "Wattleup",
            "Jandakot",
            "Yangebup",
            "South Lake",
        )
