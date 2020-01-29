
from .parish import Parish
from .database import db

class Bayswater(Parish):
    """
    The Parish of Bayswater consists of the localities of
    Embleton, Bayswater, except that portion lying
    to the east of the line of Gray Street From Jackson
    Road to Collier Road, the to the line of Jackson
    Street to Wicks Street, along Wicks Street to
    Vincent Street, and along Vincent Street to the
    railway line, together with that portion of Bedford
    lying to the south east of Beaufort Street and that
    portion of Morley lying to the south and east of Walter
    Road.
    """
    name = "Bayswater"

    @classmethod
    def generate(cls):
        bayswater = db.Localities


def bayswater():
    pass
