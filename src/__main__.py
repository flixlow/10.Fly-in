from argparse import ArgumentParser
from src.parser import Parser
from src.utils import Start, End
from src.display import Displayer
import questionary
import os


def command_line() -> str:
    parser = ArgumentParser()
    parser.add_argument("--input", default="maps/easy/01_linear_path.txt")
    parser.add_argument("--directory", default="maps")
    parser.add_argument("--selector", action="store_true")

    command_line = parser.parse_args()
    if not command_line.selector:
        return command_line.input

    current_path = os.listdir(command_line.directory)
    while(1):
        questionary


def main() -> None:
    print("\033[1;32m[START OF THE PROGRAM]\033[0m")
    file_parser = Parser(command_line())
    map = file_parser.validate()
    displayer = Displayer(map)
    displayer.display()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        raise e
        print(f"\033[1;31m[ERROR] - {type(e).__name__}\033[0m\n{e}")
    else:
        print("\033[1;32m[END OF THE PROGRAM]\033[0m")

    # for hub in map.hubs:
    #     if isinstance(hub, Start):
    #         print("\033[1;36m[START HUB]\033[0m:", hub)
    #     elif isinstance(hub, End):
    #         print("\033[1;36m[END HUB]\033[0m:", hub)
    #     else:
    #         print("\033[1;34m[HUB]\033[0m:", hub)
    # for con in map.connections:
    #     print("\033[1;35m[CONNECTION]\033[0m:", con.start.name, end=" ")
    #     print(con.end.name, con.max_link_capacity)
