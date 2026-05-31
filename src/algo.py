from src.network import Network


class Path:



class Algo:
    def __init__(self, network: Network) -> None:
        self.network = network
        self.paths: list = []
        self.max_flow: int = 0
        self.paths: list = []

    def finding(self) -> None:
        attempts = 0
        while self.max_flow > self.network.map.nb_drones:
            path = self.find_one_path()
            if path is None:
                attempts += 1
                if attempts >= 3:
                    break
            else:
                attempts = 0
                self.paths.append(path)
                self.max_flow += self.calculate_flow(path)

    def find_one_path(self):
        pass

    def calculate_flow(self, path) -> int:
        flow: int = self.network.map.nb_drones
        for current, next in path:


        return 0
