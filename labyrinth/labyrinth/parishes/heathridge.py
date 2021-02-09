from ..parish import Parish
from sqlalchemy.sql.functions import func


class Heathridge(Parish):
    """
    The Parish of Heathridge to serve the localities of
    Heathridge, Ocean Reef and Connolly.
    """

    problems = ""

    def geom(self):
        return self.locality_union("Heathridge", "Ocean Reef", "Connolly")
