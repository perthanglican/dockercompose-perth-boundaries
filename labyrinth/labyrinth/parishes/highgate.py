from ..parish import Parish
from sqlalchemy.sql.functions import func


class Highgate(Parish):
    """
    The Parish of Highgate consists of the locality of
    Highgate, and that portion of Perth that lies to the
    north of the line drawn through Stuart Street, Monger
    Street, and that portion of East Perth which lies
    to the north of the line drawn from Edward Street
    and Lord Street, and then northwards along Lord Street
    along Summer Street, then along Summer Street to the
    Swan River, and that portion of Northbridge lying
    to the west of Palmerston Street, and that portion
    of Mount Lawley lying to the south of a line drawn
    along Walcott Street to Alvan Street, then along Alvan
    Street, Park Road, along Park Road to Farnley Street,
    then along Farnley Street to Almondbury Street, and
    then along the line of Almondbury Street across the
    railway line to Guildford Road to Ellesmere Street,
    then along Ellesmere Street to the river.
    """

    code = "Highgate"
    problems = ""

    def geom(self):
        return self.get_locality_by_name("Highgate")
