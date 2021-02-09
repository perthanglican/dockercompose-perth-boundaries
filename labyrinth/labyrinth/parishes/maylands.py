from ..parish import Parish
from sqlalchemy.sql.functions import func
from .mountlawley import MountLawley


class Maylands(Parish):
    """
    The Parish of Maylands consists of the locality of Maylands
    and that portion of Mount Lawley lying to the north east
    of Third Avenue to the south west of John Street, and
    that portion of Inglewood lying to the south east of John
    Street and the line along John Street to Harcourt Road,
    and then along Harcourt Road to York Street.
    """

    problems = ""

    def geom(self):
        def cut_mount_lawley():
            return self.cut_locality(
                "Mount Lawley", (MountLawley.MTLAWLEY_JOHN_THIRD, 2)
            )

        def cut_inglewood():
            return self.cut_locality("Inglewood", (MountLawley.INGLEWOOD_JOHN_ST, 2))

        return func.ST_Union(
            self.get_locality_by_name("Maylands"),
            func.ST_Union(cut_mount_lawley(), cut_inglewood()),
        )
