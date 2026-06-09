from src.utils import Map, Hub, Connection, Zone
from functools import lru_cache


class Node:
    def __init__(self, real_hub: Hub, time: int) -> None:
        self.real_hub: Hub = real_hub
        self.time: int = time
        self.edges: list[Edge] = []
        self.passage: int = 0

    def set_previous_connection(self, connection: Connection) -> None:
        self.previous_connection: Connection = connection

    def get_remaining_capacity(self) -> int:
        return self.real_hub.max_drones - self.passage

    @staticmethod
    def is_priority_zone(edge) -> bool:
        if edge.real_connection is None:
            return False
        hub = edge.real_connection.end
        return hub.zone == Zone.PRIORITY

    def sort_edges(self) -> None:
        self.edges.sort(key=Node.is_priority_zone, reverse=True)


class Edge:
    def __init__(self, connection: Connection | None,
                 node1: Node, node2: Node) -> None:
        self.real_connection: Connection | None = connection
        self.node1: Node = node1
        self.node2: Node = node2
        self.passage: int = 0
        if self.real_connection:
            self.max_link_capacity = self.real_connection.max_link_capacity
        else:
            self.max_link_capacity = self.node1.real_hub.max_drones

    def get_remaining_capacity(self) -> int:
        return self.max_link_capacity - self.passage


class ConnectionNode(Node):
    pass


class Network:
    def __init__(self, map: Map) -> None:
        self.map: Map = map
        self.step: int = 0
        self.end_reached: bool = False
        self.nodes: dict[int, list[Node]] = {}
        self.start: Node = self.create_node(self.map.start, 0)

    @lru_cache(maxsize=None)
    def create_node(self, hub: Hub, time: int, node_type: type = Node) -> Node:
        created_node: Node = node_type(hub, time)
        self.nodes.setdefault(time, []).append(created_node)
        if hub is self.map.end:
            self.end_reached = True
        return created_node

    @lru_cache(maxsize=None)
    def create_edge(self, connection: Connection | None,
                    node1: Node, node2: Node) -> Edge:
        created_edge = Edge(connection, node1, node2)
        return created_edge

    def find_edge(self, node: Node) -> None:
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

    def next_step(self) -> None:
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
        self.step += 1
