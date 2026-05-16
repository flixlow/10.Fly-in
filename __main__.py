import sys
from parser import Parser


def main() -> None:
    av: list[str] = sys.argv
    if len(av) != 2:
        raise ValueError("pas bon les arguments de la ligne de commandes frr")
    parser = Parser(av[1])
    parser.open()


if __name__ == "__main__":
    # try:
    main()
    # except Exception as e:
    # print(f"[ERROR]: {e}")
