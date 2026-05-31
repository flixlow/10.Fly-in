from src.network import Network, Node
from collections import deque


class Algo:
    def __init__(self, network: Network) -> None:
        self.network = network
        self.paths: list = []
        self.max_flow: int = 0

    def finding(self) -> None:
        """Find paths until the number of drones can be routed."""
        attempts = 0
        max_attempts = 3
        
        while self.max_flow < self.network.map.nb_drones:
            path = self.find_one_path()
            if path is None:
                attempts += 1
                if attempts >= max_attempts:
                    break
            else:
                attempts = 0
                self.paths.append(path)
                flow = self.calculate_flow(path)
                self.max_flow += flow

    def find_one_path(self) -> list[Node] | None:
        """Find a single path from start to end using BFS."""
        queue = deque([(self.network.start, [self.network.start])])
        visited = {self.network.start}
        
        while queue:
            current_node, path = queue.popleft()
            
            # Reached the end hub
            if current_node.real_hub is self.network.map.end:
                return path
            
            # Explore edges
            for edge in current_node.edges:
                next_node = edge.node2 if edge.node1 is current_node else edge.node1
                
                # Check if next_node hasn't been visited in this path
                if next_node not in visited:
                    visited.add(next_node)
                    queue.append((next_node, path + [next_node]))
        
        return None

    def calculate_flow(self, path: list[Node]) -> int:
        """Calculate max flow for a given path."""
        min_capacity = float('inf')
        
        for i in range(len(path) - 1):
            current = path[i]
            next_node = path[i + 1]
            
            # Find the connection between these nodes
            for edge in current.edges:
                if edge.node2 is next_node or edge.node1 is next_node:
                    capacity = edge.real_connection.max_link_capacity
                    if capacity is not None:
                        min_capacity = min(min_capacity, capacity)
                    break
        
        return int(min_capacity) if min_capacity != float('inf') else 1