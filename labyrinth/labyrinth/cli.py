from .parishes import perth
from .database import DatabaseAccess
import argparse


def build(args):
    print("Building parishes:")
    db = DatabaseAccess(args.connection_string)
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--connection-string", default="postgres://postgres:postgres@localhost/perth"
    )
    subparsers = parser.add_subparsers()

    parse_build = subparsers.add_parser("build")
    parse_build.add_argument("--geojson", type=str, required=False)
    parse_build.set_defaults(func=build)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
