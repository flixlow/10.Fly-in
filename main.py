import os
import questionary
from argparse import ArgumentParser
from parser import Parser
from network import Network
from algo import DFS
from output import Output


def command_line() -> str:
    """
    The function first inspects command-line arguments for an `-i/--input`
    path. If not provided it interactively walks a directory tree using
    `questionary` until a file is selected.

    Returns
    -------
    str
        Absolute or relative path to the chosen `.txt` map file.

    Raises
    ------
    ValueError
        If the resolved file path does not end with ``.txt``.
    """
    parser = ArgumentParser()
    parser.add_argument('-i', "--input", default=None)
    parser.add_argument('-d', "--directory", default="maps")
    command_line = parser.parse_args()

    if command_line.input is not None:
        current_path = command_line.input
    else:
        current_path = command_line.directory
        while (True):
            choices = os.listdir(current_path)
            r = questionary.select("Please, select:", choices=choices).ask()
            current_path = f"{current_path}/{r}"
            if os.path.isfile(current_path):
                break

    if not current_path.endswith(".txt"):
        raise ValueError(f"File must be a .txt : {current_path}")
    return str(current_path)


def main() -> None:
    """Run the full Fly-in workflow.

    This function performs environment setup for the Pygame prompt,
    loads and validates the selected map, constructs the simulation
    network and runs the flow algorithm until either the simulation
    finishes or the desired number of drones is allocated. It then
    prints textual output and launches the visual display.
    """
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
    from display import Displayer

    file = command_line()
    file_parser = Parser(file)
    map = file_parser.validate()
    network = Network(map)
    algo = DFS(network)

    while network.is_running and not network.end_reached:
        network.next_step()

    while network.is_running and algo.max_flow < map.nb_drones:
        algo.get_max_flow()
        network.next_step()

    output = Output(map, algo)
    output.print_output()

    displayer = Displayer(map, algo.paths)
    displayer.display()


if __name__ == "__main__":
    print("\033[1;32m[START]\033[0m")
    try:
        main()
    except KeyboardInterrupt:
        print("\033[1;32m[END]\033[0m")
    except Exception as e:
        print(f"\033[1;31m[ERROR] - {type(e).__name__}\033[0m\n{e}")
    else:
        print("\033[1;32m[END]\033[0m")
