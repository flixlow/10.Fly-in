from utils import Map, Zone
from algo import DFS
from network import Edge, Node, ConnectionNode


class Drone:
    """Container representing a single drone and its assigned path.

    Parameters
    ----------
    id : int
        Zero-based drone identifier.
    path : list[(Edge, Node)]
        The time-expanded path assigned to the drone.

    Notes
    -----
    Instances are lightweight containers used by :class:`Output` to map
    algorithm paths to printable movement tokens.
    """
    def __init__(self, id: int, path: list[tuple[Edge, Node]]) -> None:
        self.id = id
        self.path = path


class Output:
    def __init__(self, map: Map, algo: DFS) -> None:
        """Create textual output for the simulation results.

        The ``Output`` object translates the algorithm's found paths and
        flows into a list of :class:`Drone` instances and prints a step-by-step
        description of movements.

        Parameters
        ----------
        map : Map
            The map instance containing start, hubs and drone count.
        algo : DFS
            The algorithm instance containing computed paths,flows and network.
        """
        self.map: Map = map
        self.algo: DFS = algo
        self.name: int = 0
        self.step: int = 0
        self.drones: list[Drone] = []
        self.len_max: int = max((len(path) for path in algo.paths), default=0)
        self.create_drones()

    def create_drones(self) -> None:
        """Instantiate Drone objects according to path flow values.

        Drones are created until the map's ``nb_drones`` count is reached.
        Each path in ``algo.paths`` is repeated according to the corresponding
        flow value in ``algo.flow_by_paths``.
        """
        for path, flow in zip(self.algo.paths, self.algo.flow_by_paths):
            for i in range(flow):
                if self.name >= self.map.nb_drones:
                    return
                self.drones.append(Drone(self.name, path))
                self.name += 1

    def add_line(self, drone: Drone) -> str:
        """Format a single drone movement token for the current step.

        The returned string includes ANSI color codes used by the existing
        output formatting and a trailing space. It handles special cases for
        restricted-zone-to-connection transitions and priority zones.

        Parameters
        ----------
        drone : Drone
            The drone whose movement at the current ``step`` is formatted.

        Returns
        -------
        str
            A formatted movement token (including ANSI codes) or the end-token
            when the drone is at its final node.
        """
        line = ""
        path = drone.path
        node = path[self.step][1]
        if self.step == (len(path) - 1):
            return f"\033[35mD{drone.id + 1}-{node.real_hub.name} "
        next_node = path[self.step + 1][1]
        if node.real_hub.zone == Zone.RESTRICTED and\
                isinstance(next_node, ConnectionNode):
            edge = path[self.step][0]
            if edge.real_connection is not None:
                connection = edge.real_connection.name
            else:
                connection = "None"
            line += f"\033[34mD{drone.id + 1}-{connection}"
        elif node.real_hub.zone == Zone.PRIORITY:
            line += f"\033[31mD{drone.id + 1}-{node.real_hub.name}"
        else:
            line += f"\033[35mD{drone.id + 1}-{node.real_hub.name}"

        line += "\033[0m "
        return line

    def print_output(self) -> None:
        """Print the formatted per-step drone movements to stdout.

        Each printed line corresponds to one time-step and contains movement
        tokens for drones that advance at that step. If the network did not
        find a solution, a warning message is printed instead.

        Returns
        -------
        None
        """
        if not self.algo.network.is_running:
            print("\033[1;38;5;208m[WARNING]\033[0m No solution was found.")
        while self.step < self.len_max:
            line = ""
            for path in self.algo.paths:
                if self.step >= len(path):
                    continue
                if path[self.step][1].real_hub is self.map.start:
                    continue
                for drone in self.drones:
                    if drone.path == path:
                        line += self.add_line(drone)
            self.step += 1
            print(line)
