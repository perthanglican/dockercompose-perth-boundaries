
from ..parish import Parish
from sqlalchemy.sql.functions import func


class RockinghamSafetyBay(Parish):
    """
    The Parish of Rockingham consists of the localities
    of East Rockinham, Rockingham, Peron, Shoalwater,
    Safety Bay, Cooloongup, Hillman, Waikiki, Baldivis,
    Warnbro and Becher.
    """
    code = 'Rockingham/Safety Bay'
    problems = "no such place as Becher, now Port Kennedy, Warnbro is another parish"

    def geom(self):
        return self.locality_union(
            'East Rockingham', 'Rockingham', 'Peron',
            'Shoalwater', 'Safety Bay', 'Cooloongup',
            'Hillman', 'Waikiki', 'Baldivis',
            'Port Kennedy')
