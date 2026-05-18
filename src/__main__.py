import sys
from src.parser import Parser


def main() -> None:
    av: list[str] = sys.argv
    if len(av) != 2:
        raise ValueError("please check input command line arguments.")
    parser = Parser(av[1])
    map = parser.validate()
    print(map)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # raise e
        print(f"\033[1;31m[ERROR]\033[0m {e}")
    else:
        print("\033[1;32m[END OF THE PROGRAM]\033[0m")
