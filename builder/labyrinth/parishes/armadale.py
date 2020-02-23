
from ..parish import Parish


class Armadale(Parish):
    """
    The Parish of Armadale consists of Forrestdale, Wungong, Armadale
    and Bedfordale.
    """
    problems = "Update required for new localities in area"

    def geom(self):
        return self.locality_union('Forrestdale', 'Wungong', 'Armadale', 'Bedfordale')
