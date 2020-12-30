
from ..parish import Parish
from sqlalchemy.sql.functions import func


class Lockridge(Parish):
    """
    The Parish of Lockrdige consists of whole of Lockridge.
    """
    problems = "textual description doesn't include Eden Hill"

    def geom(self):
        return self.locality_union('Lockridge', 'Eden Hill')
