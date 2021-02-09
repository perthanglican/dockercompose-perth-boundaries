from ..parish import Parish
from sqlalchemy.sql.functions import func


class Lesmurdie(Parish):
    """
    The Parish of Lesmurdie consists of the localities of
    Lesmurdie, Walliston, Bickley, Carmel, Pickering Brook,
    within the boundary of the Shire of Kalamunda.
    """

    problems = ""

    def geom(self):
        return self.locality_union(
            "Lesmurdie", "Walliston", "Bickley", "Carmel", "Pickering Brook"
        )
