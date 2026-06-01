from src.utils import Map, Hub, Connection
from functools import lru_cache


class Node:
    def __init__(self, real_hub: Hub, time: int) -> None:
        self.real_hub: Hub = real_hub
        self.time: int = time
        self.edges: list[Edge] = []
        self.passage: int = 0

    def get_remaining_capacity(self) -> int:
        return self.real_hub.max_drones - self.passage


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


class Network:
    def __init__(self, map: Map) -> None:
        self.map: Map = map
        self.nodes: dict[int, list[Node]] = {}
        self.start: Node = self.create_node(self.map.start, 0)
        self.step = 0
        self.end_reached: bool = False

    @lru_cache(maxsize=None)
    def create_node(self, hub: Hub, time: int) -> Node:
        created_node: Node = Node(hub, time)
        self.nodes.setdefault(time, []).append(created_node)
        if hub is self.map.end:
            self.end_reached = True
        return created_node

    def create_edge(self, connection: Connection | None,
                    node1: Node, node2: Node) -> Edge:
        created_edge = Edge(connection, node1, node2)
        return created_edge

    def find_edge(self, node: Node) -> None:
        for connection in node.real_hub.connections:
            node1 = self.create_node(connection.start, node.time + 1)
            node2 = self.create_node(connection.end, node.time + 1)

            if node1.real_hub is node.real_hub:
                new_edge = self.create_edge(connection, node, node2)
                node2.edges.append(new_edge)
                same_edge = self.create_edge(None, node, node1)
            else:
                new_edge = self.create_edge(connection, node, node1)
                same_edge = self.create_edge(None, node, node2)
                node1.edges.append(new_edge)

            node.edges.append(new_edge)
            node.edges.append(same_edge)

    def next_step(self) -> None:
        for node in self.nodes.get(self.step, []):
            self.find_edge(node)
        self.step += 1
