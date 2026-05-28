import os
import questionary  # type: ignore
from argparse import ArgumentParser
from src.network import Network
from src.parser import Parser


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
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
    from src.display import Displayer

    file = command_line()
    file_parser = Parser(file)
    map = file_parser.validate()
    network = Network(map)
    network.next_step()
    displayer = Displayer(map)
    displayer.display()


if __name__ == "__main__":
    print("\033[1;32m[START OF THE PROGRAM]\033[0m")
    try:
        main()
    except Exception as e:
        raise e
        print(f"\033[1;31m[ERROR] - {type(e).__name__}\033[0m\n{e}")
    else:
        print("\033[1;32m[END OF THE PROGRAM]\033[0m")
