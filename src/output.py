from src.utils import Map, Zone
from src.algo import DFS
from src.network import Edge, Node


class Drone:
    def __init__(self, id: int, path: list[tuple[Edge, Node]]) -> None:
        self.id = id
        self.path = path


class Output:
    def __init__(self, map: Map, algo: DFS) -> None:
        self.map: Map = map
        self.algo: DFS = algo
        self.name = 0
        self.drones: list[Drone] = []
        self.len_max: int = max((len(path) for path in algo.paths), default=0)
        self.create_drones()

    def create_drones(self) -> None:
        for path, flow in zip(self.algo.paths, self.algo.flow_by_paths):
            for i in range(flow):
                if self.name >= self.map.nb_drones:
                    return
                self.drones.append(Drone(self.name, path))
                self.name += 1

    def print_output(self) -> None:
        if not self.algo.network.is_running:
            print("\033[1;38;5;208m[WARNING]\033[0m No solution was found.")
        for step in range(self.len_max - 1):
            line = ""
            for path in self.algo.paths:
                if step + 1 >= len(path):
                    continue
                if path[step + 1][1].real_hub is self.map.start:
                    continue
                for drone in self.drones:
                    if drone.path == path:
                        node = path[step + 1][1]
                        if node.real_hub.zone == Zone.RESTRICTED and\
                                path[step][1].real_hub.zone != Zone.RESTRICTED:
                            edge = path[step + 1][0]
                            if edge.real_connection is not None:
                                connection = edge.real_connection.name
                            else:
                                connection = "None"
                            line += f"\033[34mD{drone.id + 1}-{connection}"
                        elif node.real_hub.zone == Zone.PRIORITY:
                            line += "\033[31m"
                            line += f"D{drone.id + 1}-{node.real_hub.name}"
                        else:
                            line += "\033[35m"
                            line += f"D{drone.id + 1}-{node.real_hub.name}"
                        line += "\033[0m "
            print(line)
