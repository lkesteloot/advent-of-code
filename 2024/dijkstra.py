
import heapq

# Dijkstra's shortest path.
class Dijkstra:
    # start_node: node where we start to search.
    # end_nodes: set of nodes where to stop.
    # get_neighbors(node): get list of neighbors of node.
    # get_cost(node1, node2): get cost of going from node1 to node2.
    def __init__(self, start_node, end_nodes, get_neighbors, get_cost):
        self.start_node = start_node
        self.end_nodes = end_nodes
        self.get_neighbors = get_neighbors
        self.get_cost = get_cost
        self.left_to_visit = []
        self.visited_nodes = set()
        self.cost_to_start = {}
        self.cost_to_start[start_node] = 0
        heapq.heappush(self.left_to_visit, (0, start_node))
        # Map from node to list of previous nodes.
        self.back = {}

    # Returns (cost, path).
    def go(self):
        while True:
            while True:
                value, node = heapq.heappop(self.left_to_visit)
                if node not in self.visited_nodes:
                    break

            if node in self.end_nodes:
                return (self.cost_to_start[node], self._make_path(node))

            neighbors = self.get_neighbors(node)
            cost_to_us = self.cost_to_start[node]
            for neighbor in neighbors:
                if not neighbor in self.visited_nodes:
                    cost_from_us_to_neighbor = self.get_cost(node, neighbor)
                    cost_to_neighbor = self.cost_to_start.get(neighbor)
                    cost_to_neighbor_through_us = cost_to_us + cost_from_us_to_neighbor
                    if cost_to_neighbor == None or cost_to_neighbor_through_us < cost_to_neighbor:
                        self.cost_to_start[neighbor] = cost_to_neighbor_through_us
                        heapq.heappush(self.left_to_visit, (cost_to_neighbor_through_us, neighbor))
                        self.back[neighbor] = node

    def _make_path(self, end_node):
        path = []
        node = end_node
        path.append(node)
        while node != self.start_node:
            node = self.back[node]
            path.append(node)
        path.reverse()
        return path

