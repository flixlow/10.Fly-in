from argparse import ArgumentParser, Namespace
from src.parser import Parser
from src.utils import Start, End


def command_line() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--input", default="maps/easy/01_linear_path.txt")
    return parser.parse_args()


def main() -> None:
    print("\033[1;33m[STARTING PROGRAM]\033[0m")
    command_line_parser = command_line()
    file_parser = Parser(command_line_parser.input)
    map = file_parser.validate()
    for hub in map.hubs:
        if isinstance(hub, Start):
            print("\033[1;36m[START HUB]\033[0m:", hub)
        elif isinstance(hub, End):
            print("\033[1;36m[END HUB]\033[0m:", hub)
        else:
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
