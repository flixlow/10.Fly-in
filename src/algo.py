from src.network import Network, Node, Edge
from src.utils import Zone


class DFS:
    def __init__(self, network: Network) -> None:
        self.network = network
        self.max_flow: int = 0
        self.paths: list[list[tuple[Edge, Node]]] = []
        self.flow_by_paths: list[int] = []

    """DFS based flow finder for the time-expanded network.

    Parameters
    ----------
    network : Network
        The time-expanded network on which to perform the search.

    Attributes
    ----------
    max_flow : int
        Current total flow found.
    paths : list
        List of found augmenting paths (each is a list of (Edge, Node)).
    flow_by_paths : list
        Flow value associated with each discovered path.
    """

    def add_passage(self, path: list[tuple[Edge, Node]], flow: int) -> None:
        """Apply a flow increment to all edges and nodes in ``path``.

        Parameters
        ----------
        path : list of (Edge, Node)
            Path where flow will be added.
        flow : int
            Amount of flow to add along the path.
        """
        for edge, node in path:
            edge.passage += flow
            node.passage += flow

    def get_max_flow(self) -> int:
        """Find and apply augmenting paths until no more exist.

        Returns
        -------
        int
            The updated maximum flow value.
        """
        flow: int = self.max_flow
        while path := self.find_one_path(self.network.start,
                                         [], set(), set(), set()):
            current_flow = self.get_blocking_flow(path)
            flow += current_flow
            self.add_passage(path, current_flow)
            self.paths.append(path)
            self.flow_by_paths.append(current_flow)

        self.max_flow = flow
        return flow

    def get_blocking_flow(self, path: list[tuple[Edge, Node]]) -> int:
        """Compute the blocking flow for a given path.

        The blocking flow is the minimal remaining capacity among
        the edges and destination node capacities along the path.
        """
        return min(min(
            edge.get_remaining_capacity(),
            node.get_remaining_capacity()
        ) for edge, node in path)

    def find_one_path(self, node: Node, path: list[tuple[Edge, Node]],
                      visited_nodes: set[Node], visited_edges: set[Edge],
                      dead_ends: set[Node]) -> None | list[tuple[Edge, Node]]:
        """Recursively search a single augmenting path from ``node``.

        Parameters
        ----------
        node : Node
            Current node from which to search.
        path : list
            Current path being constructed.
        visited_nodes : set
            Nodes already visited in this search branch.
        visited_edges : set
            Edges already explored in this search branch.
        dead_ends : set
            Nodes known to lead to no augmenting path.

        Returns
        -------
        list[(Edge, Node)] or None
            The found path as a list of (Edge, Node) pairs, or ``None``
            if no path exists from the current node.
        """
        if node in dead_ends:
            return None

        for edge in node.edges:
            next_node = edge.node2

            if next_node.real_hub.zone == Zone.BLOCKED:
                dead_ends.add(next_node)
                continue
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
