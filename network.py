from __future__ import annotations
from utils import Map, Hub, Connection, Zone
from functools import lru_cache


class Node:
    def __init__(self, real_hub: Hub, time: int) -> None:
        """Represents a hub instance at a given discrete time.

        Parameters
        ----------
        real_hub : Hub
            Reference to the static hub model.
        time : int
            Discrete time step this node corresponds to.
        """
        self.real_hub: Hub = real_hub
        self.time: int = time
        self.edges: list[Edge] = []
        self.passage: int = 0

    def set_previous_connection(self, connection: Connection) -> None:
        """Record the incoming connection that led to this node.

        This is used to create a waiting/connection edge for restricted
        zones.
        """
        self.previous_connection: Connection = connection

    def get_remaining_capacity(self) -> int:
        """Return remaining hub capacity (max_drones - currently used)."""
        return self.real_hub.max_drones - self.passage

    @staticmethod
    def is_priority_zone(edge: Edge) -> bool:
        """Return True if the edge leads to a priority zone.

        Args:
            edge (Edge): Edge to inspect.

        Returns:
            bool: ``True`` if the destination hub's zone is
                ``Zone.PRIORITY``, otherwise ``False``.
        """
        if edge.real_connection is None:
            return False
        hub = edge.real_connection.end
        return hub.zone == Zone.PRIORITY

    def sort_edges(self) -> None:
        """Sort outgoing edges prioritising those that lead to priority."""
        self.edges.sort(key=Node.is_priority_zone, reverse=True)


class Edge:
    def __init__(self, connection: Connection | None,
                 node1: Node, node2: Node) -> None:
        """Directed edge between two time-expanded nodes.

        If ``real_connection`` is ``None`` the edge represents waiting in the
        same hub (static transfer) and uses the hub's max_drones for capacity.
        """
        self.real_connection: Connection | None = connection
        self.node1: Node = node1
        self.node2: Node = node2
        self.passage: int = 0
        if self.real_connection:
            self.max_link_capacity = self.real_connection.max_link_capacity
        else:
            self.max_link_capacity = self.node1.real_hub.max_drones

    def get_remaining_capacity(self) -> int:
        """Return remaining capacity on this edge (link capacity - used)."""
        return self.max_link_capacity - self.passage


class ConnectionNode(Node):
    pass


class Network:
    def __init__(self, map: Map) -> None:
        """Builds and manages the time-expanded network for a Map.

        The object creates nodes and edges for each time step on demand and
        provides `next_step` to progress the expansion. It also detects
        simple infinite-expansion scenarios to stop the simulation.
        """
        self.map: Map = map
        self.step: int = 0
        self.end_reached: bool = False
        self.repetition: int = 0
        self.is_running: bool = True
        self.nodes: dict[int, list[Node | ConnectionNode]] = {}
        self.already_created: set[Hub] = set()
        self.start: Node = self.create_node(self.map.start, 0)

    @lru_cache(maxsize=None)
    def create_node(self, hub: Hub, time: int, node_type: type = Node) -> Node:
        """Create or return a cached `Node` for the given hub and time.

        The function is memoized with ``lru_cache`` so repeated requests
        for the same (hub, time) pair return the same Node instance.
        """
        created_node: Node = node_type(hub, time)
        self.nodes.setdefault(time, []).append(created_node)
        if hub is self.map.end:
            self.end_reached = True
        return created_node

    @lru_cache(maxsize=None)
    def create_edge(self, connection: Connection | None,
                    node1: Node, node2: Node) -> Edge:
        """Create or return a cached `Edge` between two nodes.

        Edges are created with an optional underlying ``Connection`` which
        determines link capacity and semantics.
        """
        created_edge = Edge(connection, node1, node2)
        return created_edge

    def find_edge(self, node: Node) -> None:
        """edges for a time-expanded node from its real hub connections.

        For each :class:`Connection` associated with the node's real hub:
        - creates a waiting edge from the node to the same hub at t + 1;
        - creates a movement edge from the node to the connected hub at t + 1;
        - records the connection that led to the new node;
        - appends both edges to ``node.edges``;
        - sorts the outgoing edges to prefer priority zones.

        Args:
            node (Node): The time-expanded node.

        Returns:
            None
        """
        for connection in node.real_hub.connections:
            if node.real_hub is connection.start:
                start = connection.start
                end = connection.end
            else:
                start = connection.end
                end = connection.start

            static_node = self.create_node(start, node.time + 1)
            static_edge = self.create_edge(None, node, static_node)
            new_node = self.create_node(end, node.time + 1)
            new_edge = self.create_edge(connection, node, new_node)

            new_node.set_previous_connection(connection)
            node.edges.append(new_edge)
            node.edges.append(static_edge)
        node.sort_edges()

    def verify_infinite_loop(self) -> None:
        """Detect repeated expansion without progress and stop the run.

        The method compares the set of hubs created at the current step
        to previously seen hubs and flags repeated patterns.
        """
        last_created = set(
            node.real_hub for node in self.nodes.get(self.step, []))
        if last_created.issubset(self.already_created):
            if self.repetition > 3:
                self.is_running = False
                return
            self.repetition += 1
        else:
            self.repetition = 0
            self.already_created.update(last_created)

    def next_step(self) -> None:
        """Expand the network by one time step.

        For each node at the current step add waiting and connection
        edges for the following time-step. If the end hub hasn't been
        reached, run the infinite-loop verification logic.
        """
        for node in self.nodes.get(self.step, []):
            if not isinstance(node, ConnectionNode)\
                    and node.real_hub.zone == Zone.RESTRICTED:
                new_node = self.create_node(
                    node.real_hub, node.time + 1, ConnectionNode)
                new_edge = self.create_edge(
                    node.previous_connection, node, new_node)
                node.edges.append(new_edge)
            else:
                self.find_edge(node)

        if not self.end_reached:
            self.verify_infinite_loop()
        self.step += 1
