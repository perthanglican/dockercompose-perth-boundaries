
from ..parish import Parish
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
    code = 'Mount Lawley'
    problems = "Mount Lawley gazetted boundary is no longer at Walcott"
    INGLEWOOD_JOHN_ST = ('Inglewood - John St', [[
        83654986,
        83660734,
        83660735,
        83660736,
        83660737,
        83660738,
        83660739,
        83660740,
        83654972,
        83654979,
        83654980,
        83656578,
        83653697,
        83653698,
        83653699,
        83638245,
    ]])
    INGLEWOOD_DUNDAS = ('Inglewood - Dundas St', [[
        83653781,
        83653780,
        83653710,
        83653709,
        83653708,
        83653707,
        83653706,
        83653705,
    ],[
        83653717,
        83653716,
        83653715,
        83653714,
        83653712,
        83653711,
        83653672,
        83653691
    ]])
    MTLAWLEY_LONGROYD_NORTH_WALCOTT = ('Mt Lawley - Longroyd, ...', [[
        83653691,
        83653690,
        83653689,
        83653688,
        83653687,
        83653686,
        83653685,
        83653684,
        83653683,
        83653682,
        83653679,
        83653678,
        83653677,
    ],[
        83667029,
        83667030,
        83667031,
        83667032,
        83667033,
        83667034,
        83667035,
        83667036,
        83667037,
        83667038,
        83667039,
        83667040,
        83667041,
        83667042,
        83667043,
        83667044,
        83667045,
        83667046,
        83667047,
        83667048,
        83667049,
        83667050,
    ],[
        83667206,
        83667207,
        83748909,
        83748910,
    ],[
        83639602,
        83639601,
        (115.88517,-31.93866),
    ]])
    MTLAWLEY_JOHN_THIRD = ('Mt Lawley - John, Third St, ...', [[
        83660734,
        83654986,
        83654985,
        83654984,
    ], [
        83654842,
        83654842,
        83654844,
        83654845,
        83639421,
        83639420,
    ]])

    def geom(self):
        def cut_bedford():
            return self.cut_locality('BEDFORD', (Bayswater.BEDFORD_BEAUFORT_ST, 1))

        def cut_inglewood():
            return self.cut_locality('Inglewood', (self.INGLEWOOD_JOHN_ST, 1), (self.INGLEWOOD_DUNDAS, 1))

        def cut_mount_lawley():
            return self.cut_locality(
                'Mount Lawley',
                (self.MTLAWLEY_JOHN_THIRD, 1),
                (self.MTLAWLEY_LONGROYD_NORTH_WALCOTT, 1))

        return func.ST_Buffer(func.ST_Union(
            func.ST_Union(
                cut_bedford(),
                cut_inglewood()),
                cut_mount_lawley()), 0.1)
