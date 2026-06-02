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
        while path := self.find_one_path():
            flow += (current_flow := self.get_blocking_flow(path))
            self.add_passage(path, current_flow)
            self.paths.append(path)

        self.max_flow = flow
        return flow

    def get_blocking_flow(self, path: list[Node | Edge]) -> int:
        return min(item.get_remaining_capacity() for item in path)

    def find_one_path(self) -> list[Node | Edge] | None:
        start = self.network.start
        queue = deque([start])
        visited: set[Node] = {start}
        parent: dict[Node, tuple[Node, Edge]] = {}

        while queue:
            node = queue.popleft()
            for edge in node.edges:
                if edge.get_remaining_capacity() <= 0:
                    continue

                next_node = edge.node1 if node is not edge.node1 else edge.node2
                if next_node.time <= node.time:
                    continue
                if next_node.get_remaining_capacity() <= 0:
                    continue
                if next_node in visited:
                    continue

                visited.add(next_node)
                parent[next_node] = (node, edge)
                if next_node.real_hub is self.network.map.end:
                    return self._reconstruct_path(start, next_node, parent)

                queue.append(next_node)

        return None

    def _reconstruct_path(self, start: Node, end: Node,
                          parent: dict[Node, tuple[Node, Edge]]) -> list[Node | Edge]:
        path: list[Node | Edge] = [end]
        current = end

        while current is not start:
            prev_node, edge = parent[current]
            path.append(edge)
            path.append(prev_node)
            current = prev_node

        return list(reversed(path))
