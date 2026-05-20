from argparse import ArgumentParser
from src.parser import Parser
# from src.utils import Start, End
from src.display import Displayer
import questionary
import os


def command_line() -> str:
    parser = ArgumentParser()
    parser.add_argument("--input", default=None)
    parser.add_argument("--directory", default="maps")
    command_line = parser.parse_args()

    current_path: str = command_line.directory
    while (True):
        choices = os.listdir(current_path)
        r = questionary.select("Please, select:", choices=choices).ask()
        current_path = f"{current_path}/{r}"
        if os.path.isfile(current_path):
            break

    if command_line.input is not None:
        current_path = command_line.input

    if not current_path.endswith(".txt"):
        raise ValueError(f"File must be a .txt : {current_path}")
    return current_path


def main() -> None:
    print("\033[1;32m[START OF THE PROGRAM]\033[0m")
    file = command_line()
    print(file)
    file_parser = Parser(file)
    map = file_parser.validate()
    displayer = Displayer(map)
    displayer.display()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # raise e
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
