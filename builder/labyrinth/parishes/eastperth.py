
from ..parish import Parish
from sqlalchemy.sql.functions import func


class EastPerth(Parish):
    """
    The Parish of East Perth consists of....
    """
    code = 'East Perth'
    problems = "Textual description missing"

    def geom(self):
        return self.get_locality_by_name('East Perth')
