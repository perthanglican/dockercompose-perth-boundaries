
from ..parish import Parish
from sqlalchemy.sql.functions import func


class Joondalup(Parish):
    """
    The Parish of Ellenbrook consists of....
    """
    problems = "Textual description missing"

    def geom(self):
        return self.get_locality_by_name('Joondalup')
