import sys
from src.parser import Parser


def main() -> None:
    print("\033[1;33m[STARTING PROGRAM]\033[0m")
    av: list[str] = sys.argv
    if len(av) != 2:
        raise ValueError("please check input command line arguments.")
    parser = Parser(av[1])
    map = parser.validate()
    for hub in map.hubs:
        print("\033[1;34m[HUB]\033[0m:", hub)
    for con in map.connections:
        print("\033[1;35m[CONNECTION]\033[0m:", con.start.name, end=" ")
        print(con.end.name, con.max_link_capacity)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # raise e
        print(f"\033[1;31m[ERROR] - {type(e).__name__}\033[0m\n{e}")
    else:
        print("\033[1;32m[END OF THE PROGRAM]\033[0m")
