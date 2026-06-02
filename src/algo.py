from src.network import Network, Node, Edge


class DFS:
    def __init__(self, network: Network) -> None:
        self.network = network
        self.max_flow: int = 0
        self.paths: list = []

    def add_passage(self, path: list[Node | Edge], flow: int) -> None:
        for item in path:
            item.passage += flow

    def get_max_flow(self) -> int:
        flow: int = self.max_flow
        while path := self.find_one_path(self.network.start, [], set()):
            flow += (current_flow := self.get_blocking_flow(path))
            self.add_passage(path, current_flow)
            self.paths.append(path)

        self.max_flow = flow
        return flow

    def get_blocking_flow(self, path: list[Node | Edge]) -> int:
        return min(item.get_remaining_capacity() for item in path)

    def find_one_path(self, node: Node,
                      path: list[Node | Edge],
                      visited: set[Node | Edge]):
        for edge in node.edges:
            next_node = edge.node1 if node != edge.node1 else edge.node2
            if edge in visited or next_node in visited:
                continue
            if edge.get_remaining_capacity() <= 0:
                continue
            if next_node.get_remaining_capacity() <= 0:
                continue
            if next_node.time <= node.time:
                continue

            path.append(edge)
            path.append(next_node)
            visited.add(edge)
            visited.add(next_node)
            if next_node.real_hub is self.network.map.end:
                return path

            new_path = self.find_one_path(next_node, path, visited)

            if new_path:
                return new_path
            else:
                path.pop()
                path.pop()
                visited.remove(edge)
                visited.remove(next_node)

        return None
