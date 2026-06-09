from src.utils import Map
from src.algo import DFS


class Drone:
    def __init__(self, id: int, path: list[tuple]) -> None:
        self.id = id
        self.path = path


def output_format(map: Map, algo: DFS) -> None:
    name = 0
    drones: list[Drone] = []
    for path, flow in zip(algo.paths, algo.flow_by_paths):
        for i in range(flow):
            if name >= map.nb_drones:
                return
            drones.append(Drone(name, path))
            name += 1

    len_max = max(len(path) for path in algo.paths)
    for step in range(len_max - 1):
        line = ""
        for path in algo.paths:
            if step + 1 >= len(path):
                continue
            if path[step + 1][1].real_hub is map.start:
                continue
            for drone in drones:
                if drone.path == path:
                    hub_name = path[step + 1][1].real_hub.name
                    line += f"D{drone.id + 1}-{hub_name} "
        print(line)
