from ..parish import Parish
from sqlalchemy.sql.functions import func


class Wanneroo(Parish):
    """
    The Parish of Wanneroo/Yanchep consists of the localities of Wannneroo,
    Wangarra, Edgewater, Joondalup, Burns, Yanchep, Quinns Rocks, Mariginiup,
    and all other localities in the Shire of Wanneroo.
    """

    problems = (
        "all other localities in Wanneroo not implemented; Burns is now Burns Beach"
    )

    def geom(self):
        return self.locality_union(
            "Wanneroo",
            "Edgewater",
            "Joondalup",
            "Burns Beach",
            "Yanchep",
            "Quinns Rocks",
            "Mariginiup",
        )
