
from ..parish import Parish
from sqlalchemy.sql.functions import func


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
    problems = "Locality of Bayswater boundary relies on non-existant roads"

    MORLEY_WALTER_RD = ('Morley - along Walter Road',
        [[83637447, 83637448, 83637449, 83637450, 83637451, 83637452, 83637453, 83637454, 83637455, 83637456, 83637457, 83637458, 83637459, 83637460, 83637461, 83637462, 83637462, 83637463, 83637464, 83637465, 83639344, 83639345, 83639341]])
    BEDFORD_BEAUFORT_ST = ('Bedford - along Beaufort Street', [[83653651, 83637437, 83637438, 83637439, 83637431, 83637432, 83637433, 83637434, 83637435, 83637436, 83637543, 83637544, 83637545, 83637531]])
    BAYSWATER_GREY_ST = ('Bayswater - along Grey Street', [[
        83638166,
        83638165,
        83638164,
        83638163,
        83638162,
        83638161,
        83638160,
        83638159,
        83639342,
        83638843]])

    def geom(self):
        def cut_morley():
            return self.cut_locality('MORLEY', (self.MORLEY_WALTER_RD, 2))

        def cut_bedford():
            return self.cut_locality('BEDFORD', (self.BEDFORD_BEAUFORT_ST, 2))

        def cut_bayswater():
            return self.cut_locality('BAYSWATER', (self.BAYSWATER_GREY_ST, 1))

        morley = cut_morley()
        bayswater = cut_bayswater()
        embleton = self.get_locality_by_name('EMBLETON')
        bedford = cut_bedford()

        return func.ST_Union(
            func.ST_Union(
                func.ST_Union(
                    bedford,
                    bayswater),
                embleton),
            morley)
