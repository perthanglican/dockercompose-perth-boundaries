
from ..parish import Parish
from sqlalchemy.sql.functions import func


class Fremantle(Parish):
    """
    The Parish of Fremantle consists of the localities of Fremantle, North
    Fremantle, East Fremantle, Palmyra, Beaconsfield, and that portion of
    Hamilton Hill that lies to the west of Carrington Street and north of
    Rockingham road.
    """
    problems = ""

    HAMILTON_CARRINGTON = ('Hamilton Hill - along Carrington / Rockingham Rd', [
        [
            # Rockingham Road
            83591747,
            83591748,
            83591749,
            83591750,
            83591751,
            83591752,
            83591753,
            83591754,
            83591756,
            83591757,
            83591758,
            83591759,
        ], [
            # Carrington
            83590002,
            83590001,
            83590000,
            83589999,
            83589998,
            83589997,
            83589996,
            83589995,
            83645959
        ]])

    def geom(self):
        def cut_hamilton_hill():
            return self.cut_locality('Hamilton Hill', (self.HAMILTON_CARRINGTON, 2))

        return func.ST_Union(
            self.locality_union(
                'Fremantle', 'North Fremantle', 'East Fremantle', 'Palmyra', 'Beaconsfield'),
            cut_hamilton_hill())

