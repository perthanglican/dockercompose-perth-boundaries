
from ..parish import Parish
from sqlalchemy.sql.functions import func


class Ellenbrook(Parish):
    """
    The Parish of Ellenbrook consists of....
    """
    problems = "Textual description missing"

    def geom(self):
        return self.get_locality_by_name('Ellenbrook')
