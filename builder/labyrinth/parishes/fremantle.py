
from ..parish import Parish, Cut, RoadPath
from sqlalchemy.sql.functions import func


class Fremantle(Parish):
    """
    The Parish of Fremantle consists of the localities of Fremantle, North
    Fremantle, East Fremantle, Palmyra, Beaconsfield, and that portion of
    Hamilton Hill that lies to the west of Carrington Street and north of
    Rockingham road.
    """
    problems = ""

    HAMILTON_CARRINGTON = Cut(
        'Hamilton Hill - along Carrington / Rockingham Rd',
        # Rockingham Road
        RoadPath('1030498/1-S', '1030498/2-S', '1030498/3-S', '1030498/4-S', '1030498/5-S', '1030498/6-S', '1030498/90-S', '1030498/91-S', '1030498/9-S', '1030498/10-S', '1030498/11-S', '1030498/75-S'),
        # Carrington
        RoadPath('1030001/36-S', '1030001/35-S', '1030001/34-S', '1030001/8-S', '1030001/33-S', '1030001/32-S', '1030001/24-S', '1030001/23-S', '1180004/19-S'))

    def geom(self):
        def cut_hamilton_hill():
            return self.cut_locality('Hamilton Hill', (self.HAMILTON_CARRINGTON, 2))

        return func.ST_Union(
            self.locality_union(
                'Fremantle', 'North Fremantle', 'East Fremantle', 'Palmyra', 'Beaconsfield'),
            cut_hamilton_hill())

