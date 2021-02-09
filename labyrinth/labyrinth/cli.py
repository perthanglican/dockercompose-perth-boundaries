from .parishes import perth
from .database import DatabaseAccess
from .dump import to_json as dump_to_json
import json
import argparse


def build(args):
    print("Building parishes:")
    db = DatabaseAccess(args.connection_string)
    db.cleanup()
    for parish in perth:
        problems = getattr(parish, "problems", "")
        if problems and problems != "":
            print(
                "  {:>30}: {}".format(
                    parish.get_code(), getattr(parish, "problems", "")
                )
            )
        parish(db).generate()
    print("{} parishes generated.".format(len(perth)))


def dump(args):
    db = DatabaseAccess(args.connection_string)
    obj = dump_to_json(db)
    with open(args.path, "w") as fd:
        json.dump(obj, fd)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--connection-string", default="postgres://postgres:postgres@localhost/perth"
    )
    subparsers = parser.add_subparsers()

    parse_build = subparsers.add_parser("build")
    parse_build.set_defaults(func=build)

    parse_dump = subparsers.add_parser("dump")
    parse_dump.add_argument("path", type=str)
    parse_dump.set_defaults(func=dump)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
