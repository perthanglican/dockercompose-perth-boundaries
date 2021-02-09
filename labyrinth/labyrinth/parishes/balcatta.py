from ..parish import Parish


class BalcattaHammersley(Parish):
    """
    The Parish of Balcatta/Hammersley consists of the
    localities of Hamersley, Balcatta and Stirling.
    """

    code = "Balcatta/Hamersley"
    problems = ""

    def geom(self):
        return self.locality_union("Balcatta", "Hamersley", "Stirling")
