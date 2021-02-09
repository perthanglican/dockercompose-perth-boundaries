from ..parish import Parish
from sqlalchemy.sql.functions import func


class Guildford(Parish):
    """
    The Parish of Guildford consists of South
    Guildford, Guildford, Hazelmere, Pyrton and
    Caversham.
    """

    problems = "There is no such place as Pyrton"

    def geom(self):
        return self.locality_union(
            "South Guildford", "Guildford", "Hazelmere", "Caversham"
        )
