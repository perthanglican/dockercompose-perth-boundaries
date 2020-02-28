
from ..parish import Parish, Cut, RoadPath
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

    MORLEY_WALTER_RD = Cut(
        'Morley - along Walter Road',
        RoadPath('1120003/7-S', '1120003/8-L', '1120003/9-L', '1120003/10-L', '1120003/11-L', '1120003/12-L', '1120003/13-L', '1120003/36-S', '1120003/16-S', '1120003/17-S', '1120003/18-S', '1120003/19-S', '1120003/20-S', '1120003/21-S', '1120003/22-S', '1120003/23-S', '1120003/23-S', '1120003/24-S', '1120003/25-S', '1120003/26-S', '1120656/1-S', '1120656/2-S', '1120655/1-S'))

    BEDFORD_BEAUFORT_ST = Cut(
        'Bedford - along Beaufort Street',
        RoadPath('1250050/26-R', '1120002/13-R', '1120002/14-R', '1120002/15-R', '1120002/22-S', '1120002/6-S', '1120002/7-S', '1120002/8-S', '1120002/9-S', '1120002/20-S', '1120006/19-R', '1120006/20-R', '1120006/21-R', '1120006/6-S'))

    BAYSWATER_GREY_ST = Cut(
        'Bayswater - along Grey Street',
        RoadPath('1120079/7-S', '1120079/6-S', '1120079/5-S', '1120079/4-S', '1120079/9-S', '1120079/8-S', '1120079/2-S', '1120079/1-S', '1120655/2-S', '1120369/1-S'))

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
