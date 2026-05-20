from src.utils import Map


class PathFinder:
    def __init__(self, map: Map) -> None:
        self.map: Map = map
        self.sim_is_running: bool = True

    def find(self) -> None:
        ...
        # while(self.sim_is_running):
