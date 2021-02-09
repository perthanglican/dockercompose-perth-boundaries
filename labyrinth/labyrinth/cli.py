from .parishes import perth
from .database import DatabaseAccess


def main():
    print("Building parishes:")
    db = DatabaseAccess("postgres://postgres:postgres@localhost/perth")
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


if __name__ == "__main__":
    main()
