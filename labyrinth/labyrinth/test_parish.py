from .geometry import Suture, GeoJSONPath
import json


class DummyPath(GeoJSONPath):
    def __init__(self, path):
        self._test_path = path

    def _get_path(self, _db):
        return self._test_path


def make_crs(typ, path):
    return {
        "type": typ,
        "crs": {"type": "name", "properties": {"name": "EPSG:3857"},},
        "coordinates": path,
    }


def r(l):
    return list(reversed(l))


def eq(o1, exp):
    l = o1.get_path(None)["coordinates"]
    print("l=", l)
    print("exp=", exp)
    return (l == exp) or (r(l) == exp)


def check_expected(l1, l2, expected):
    assert eq(Suture(DummyPath(make_crs("MultiLineString", [l1, l2]))), expected)
    assert eq(Suture(DummyPath(make_crs("MultiLineString", [r(l1), l2]))), expected)
    assert eq(Suture(DummyPath(make_crs("MultiLineString", [l1, r(l2)]))), expected)
    assert eq(Suture(DummyPath(make_crs("MultiLineString", [r(l1), r(l2)]))), expected)


def test_a():
    expected = [[1, 2], [2, 2], [2, 2], [1, 2], [8, 8]]
    l1 = [[2, 2], [1, 2], [8, 8]]
    l2 = [[1, 2], [2, 2]]
    check_expected(l1, l2, expected)
