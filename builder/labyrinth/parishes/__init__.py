from os.path import dirname, basename, isfile, join
from ..parish import Parish
import glob
import importlib


def scan_modules():
    modules = [
        basename(f)[:-3]
        for f in glob.glob(join(dirname(__file__), "*.py"))
        if isfile(f) and not f.endswith('__init__.py')]

    def find_parishes(mod):
        objs = []
        for nm in dir(mod):
            if nm.startswith('__'):
                continue
            obj = getattr(mod, nm)
            try:
                if issubclass(obj, Parish) and obj is not Parish:
                    objs.append(obj)
            except TypeError:
                pass
        return objs

    classes = []
    for pmod in modules:
        mod = importlib.import_module('.' + pmod, 'labyrinth.parishes')
        classes += find_parishes(mod)
    return sorted(set(classes), key=lambda x: x.get_code())


perth = scan_modules()
