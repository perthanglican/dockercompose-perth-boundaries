from ..parish import Parish
from ..geometry import Cut, RoadPath, LatLngPath, Suture
from sqlalchemy.sql.functions import func
from .bayswater import Bayswater


class MountLawley(Parish):
    """
    The Parish of Mount Lawley consists of the localities of:

    a. Bedford, except for that portion lying to the South
    East of Beaufort Street
    b. Inglewood, except for that portion lying to the
    South East of John Street and that portion bounded
    by Dundas Street, Hamer Parade and Walter Road West.
    c. Mount Lawley, except for that portion lying to
    the North West of Longroyd Street - North Street,
    and that portion lying to the South East of John
    Street and the North East of Third Avenue.
    """

    code = "Mount Lawley"
    problems = "Mount Lawley gazetted boundary is no longer at Walcott"
    INGLEWOOD_JOHN_ST = Cut(
        "Inglewood - John St",
        Suture(
            RoadPath(
                "1250282/5-S",
                "1253029/1-S",
                "1253029/2-S",
                "1253029/3-S",
                "1253029/4-S",
                "1253029/5-S",
                "1253029/6-S",
                "1253029/7-S",
                "1250278/2-S",
                "1250281/1-S",
                "1250281/2-S",
                "1250868/18-S",
                "1250056/6-S",
                "1250056/7-S",
                "1250056/8-S",
                "1120096/10-S",
            )
        ),
    )
    INGLEWOOD_DUNDAS = Cut(
        "Inglewood - Dundas St",
        Suture(
            RoadPath(
                "1250060/10-S",
                "1250057/11-S",
                "1250057/10-S",
                "1250057/9-S",
                "1250057/8-S",
            ),
            RoadPath(
                "1250058/7-S",
                "1250058/6-S",
                "1250058/5-S",
                "1250058/4-S",
                "1250058/2-S",
                "1250058/1-S",
                "1250052/9-S",
                "1250055/12-S",
            ),
        ),
    )
    MTLAWLEY_LONGROYD_NORTH_WALCOTT = Cut(
        "Mt Lawley - Longroyd, ...",
        RoadPath(
            "1250055/12-S",
            "1250055/11-S",
            "1250055/7-S",
            "1250055/10-S",
            "1250055/9-S",
            "1250055/5-S",
            "1250055/4-S",
            "1250055/3-S",
            "1250055/2-S",
            "1250055/1-S",
            "1250053/3-S",
            "1250053/2-S",
            "1250053/1-S",
        ),
        RoadPath(
            "1300281/5-S",
            "1300281/6-S",
            "1300281/7-S",
            "1300281/8-S",
            "1300281/9-S",
            "1300281/10-S",
            "1300281/11-S",
            "1300281/12-S",
            "1300281/25-S",
            "1300281/26-S",
            "1300281/24-S",
            "1300281/16-S",
            "1300281/17-S",
            "1300281/18-S",
            "1300281/19-S",
            "1300281/20-S",
            "1300281/21-S",
            "1300281/22-S",
            "1300281/23-S",
        ),
        RoadPath("1300292/7-R", "1300292/8-R", "H026/6-S", "H026/7-S"),
        Suture(
            RoadPath("1120762/2-S", "1120762/1-S"), LatLngPath([115.88534, -31.93881])
        ),
    )
    MTLAWLEY_JOHN_THIRD = Cut(
        "Mt Lawley - John, Third St, ...",
        Suture(
            RoadPath("1253029/1-S", "1250282/5-S", "1250282/15-S", "1250282/14-S"),
            RoadPath(
                "1250223/6-S",
                "1250223/9-S",
                "1250223/10-S",
                "1250223/8-S",
                "1120708/2-S",
                "1120708/1-S",
            ),
        ),
    )

    def geom(self):
        def cut_bedford():
            return self.cut_locality("BEDFORD", (Bayswater.BEDFORD_BEAUFORT_ST, 1))

        def cut_inglewood():
            return self.cut_locality(
                "Inglewood", (self.INGLEWOOD_JOHN_ST, 1), (self.INGLEWOOD_DUNDAS, 1)
            )

        def cut_mount_lawley():
            return self.cut_locality(
                "Mount Lawley",
                (self.MTLAWLEY_JOHN_THIRD, 1),
                (self.MTLAWLEY_LONGROYD_NORTH_WALCOTT, 1),
            )

        return func.ST_Buffer(
            func.ST_Union(
                func.ST_Union(cut_bedford(), cut_inglewood()), cut_mount_lawley()
            ),
            0.1,
        )
