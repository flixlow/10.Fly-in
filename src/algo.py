from src.network import Network, Node, Edge


class DFS:
    def __init__(self, network: Network) -> None:
        self.network = network
        self.max_flow: int = 0
        self.paths: list = []

    def find_one_path(self, starting_node: Node,
                      path: list[Node | Edge],
                      visited: list[Node | Edge],):
        for edge in starting_node.edges:
            next_node = edge.node1 if starting_node != edge.node1 else edge.node2
            if edge.get_remaining_capacity() <= 0 and edge not in visited:
                continue
            elif next_node.get_remaining_capacity() <= 0\
                    and next_node not in visited:
                continue
            elif next_node.time <= starting_node.time:
                continue

            path.append(edge)
            path.append(next_node)
            if next_node.real_hub is self.network.map.end:
                return path
            path_len: int = len(path)
            new_path = self.find_one_path(next_node, path, visited)

            if new_path:
                return new_path
            else:
                visited.append(edge)
                visited.append(next_node)
                del path[path_len:]

        return None

    # def finding(self) -> None:
    #     attempts = 0
    #     while self.max_flow > self.network.map.nb_drones:
    #         path = self.find_one_path()
    #         if path is None:
    #             attempts += 1
    #             if attempts >= 3:
    #                 break
    #         else:
    #             attempts = 0
    #             self.paths.append(path)
    #             self.max_flow += self.calculate_flow(path)

    # def calculate_flow(self, path: list[Node]) -> int:
    #     flow: int = self.network.map.nb_drones

    #     for current, next in zip(path, path[1:]):
    #         for edge in current.edges:
    #             if edge.node1 is next or edge.node2 is next:
    #                 flow = min(flow, edge.real_connection.max_link_capacity)
    #                 break

    # flow = min(flow, current.real_hub.max_drones, next.real_hub.max_drones)

    #     return flow
