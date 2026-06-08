from src.network import Network, Node, Edge


class DFS:
    def __init__(self, network: Network) -> None:
        self.network = network
        self.max_flow: int = 0
        self.paths: list = []

    def add_passage(self, path: list[tuple[Edge, Node]], flow: int) -> None:
        for edge, node in path:
            edge.passage += flow
            node.passage += flow

    def get_max_flow(self) -> int:
        flow: int = self.max_flow
        while path := self.find_one_path(self.network.start,
                                         [], set(), set(), set()):
            current_flow = self.get_blocking_flow(path)
            flow += current_flow
            self.add_passage(path, current_flow)
            self.paths.append(path)

        self.max_flow = flow
        return flow

    def get_blocking_flow(self, path: list[tuple[Edge, Node]]) -> int:
        return min(min(
            edge.get_remaining_capacity(),
            node.get_remaining_capacity()
        ) for edge, node in path)

    def find_one_path(self, node: Node,
                      path: list[tuple[Edge, Node]],
                      visited_nodes: set[Node],
                      visited_edges: set[Edge],
                      dead_ends: set[Node]
                      ) -> None | list[tuple]:
        if node in dead_ends:
            return None

        for edge in node.edges:  # sort by priority
            next_node = edge.node2

            if next_node.time <= node.time:
                continue

            if edge.get_remaining_capacity() <= 0:
                continue

            if edge in visited_edges:
                continue

            if next_node.get_remaining_capacity() <= 0:
                continue

            visited_nodes.add(node)
            visited_edges.add(edge)
            path.append((edge, next_node))

            if next_node.real_hub is self.network.map.end:
                return path
            new_path = self.find_one_path(next_node, path, visited_nodes,
                                          visited_edges, dead_ends)
            if new_path:
                return new_path
            else:
                path.pop()
                visited_edges.remove(edge)
                visited_nodes.remove(node)
        dead_ends.add(node)
        return None
