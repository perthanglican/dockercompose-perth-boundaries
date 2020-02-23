
from ..parish import Parish
from sqlalchemy.sql.functions import func


class Kwinana(Parish):
    """
    The Parish of Kwinana consists of the localities of Medina, Orelia, Calista,
    Kwinana Town Centre, Naval Base, Kwinana Base, Postans, Hope Valley, The
    Spectacles, Mandogalup, Wandi, Anketell, Casuarina, Leda and Wellard.
    """
    problems = "Kwinana Base should be Kwinana Beach"

    def geom(self):
        return self.locality_union(
            'Medina', 'Calista', 'Kwinana Town Centre', 'Naval Base', 'Kwinana Beach',
            'Postans', 'Hope Valley', 'The Spectacles', 'Mandogalup', 'Wandi',
            'Anketell', 'Casuarina', 'Leda', 'Wellard')
