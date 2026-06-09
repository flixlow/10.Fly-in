from src.utils import Map, Zone, Drone
from src.algo import DFS


class Output:
    def __init__(self, map: Map, algo: DFS) -> None:
        self.map: Map = map
        self.algo: DFS = algo
        self.name = 0
        self.drones: list[Drone] = []
        self.len_max = max(len(path) for path in algo.paths)
        self.create_drones()

    def create_drones(self) -> None:
        for path, flow in zip(self.algo.paths, self.algo.flow_by_paths):
            for i in range(flow):
                if self.name >= self.map.nb_drones:
                    return
                self.drones.append(Drone(self.name, path))
                self.name += 1

    def print_output(self) -> None:
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
                            connection = edge.real_connection.name
                            line += "\033[34m"
                            line += f"D{drone.id + 1}-{connection}"
                        else:
                            line += "\033[35m"
                            line += f"D{drone.id + 1}-{node.real_hub.name}"
                        line += "\033[0m "
            print(line)
