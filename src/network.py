from src.utils import Map, Hub, Connection
from functools import lru_cache


class Node:
    def __init__(self, real_hub: Hub, time: int) -> None:
        self.real_hub: Hub = real_hub
        self.edges: list[Edge] = []
        self.time: int = time


class Edge:
    def __init__(self, connection: Connection,
                 node1: Node, node2: Node) -> None:
        self.real_connection: Connection = connection
        self.node1: Node = node1
        self.node2: Node = node2


class Network:
    def __init__(self, map: Map) -> None:
        self.map: Map = map
        self.nodes: dict[int, list[Node]] = {}
        self.start: Node = self.create_node(self.map.start, 0)
        self.step = 0

    @lru_cache(maxsize=None)
    def create_node(self, hub: Hub, time: int) -> Node:
        created_node: Node = Node(hub, time)
        self.nodes.setdefault(time, []).append(created_node)
        return created_node

    def create_edge(self, connection: Connection,
                    node1: Node, node2: Node) -> Edge:
        created_edge = Edge(connection, node1, node2)
        return created_edge

    def next_step(self) -> None:
        for node in self.nodes.get(self.step, []):
            self.find_edge(node)
        self.step += 1

    def find_edge(self, node: Node) -> None:
        for connection in node.real_hub.connections:
            node1 = self.create_node(connection.start, node.time + 1)
            node2 = self.create_node(connection.end, node.time + 1)

            if node1 is node.real_hub:
                new_edge = self.create_edge(connection, node1, node2)
            else:
                new_edge = self.create_edge(connection, node2, node1)
            node1.edges.append(new_edge)
            node2.edges.append(new_edge)
