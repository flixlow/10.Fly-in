import sys
from src.parser import Parser


def main() -> None:
    av: list[str] = sys.argv
    if len(av) != 2:
        raise ValueError("please check input command line arguments.")
    parser = Parser(av[1])
    map = parser.validate_and_parse()
    for hub in map.hubs:
        print(hub)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n\033[1;31m[ERROR]\033[0m\n{e}")
