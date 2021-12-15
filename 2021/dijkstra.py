
import heapq

# Dijkstra's shortest path.
class Dijkstra:
    # start_node: node where we start to search.
    # end_node: node where to stop.
    # max_value: value larger than sum of all possible costs.
    # get_neighbors(node): get list of neighbors of node.
    # get_cost(node1, node2): get cost of going from node1 to node2.
    def __init__(self, start_node, end_node, max_value, get_neighbors, get_cost):
        self.start_node = start_node
        self.end_node = end_node
        self.max_value = max_value
        self.get_neighbors = get_neighbors
        self.get_cost = get_cost
        self.h = []
        self.visited = set()
        self.distance = {}
        self.distance[start_node] = 0
        heapq.heappush(self.h, (0, start_node))
        # Map from node to the previous node.
        self.back = {}

    # Returns (cost, path).
    def go(self):
        while True:
            while True:
                value, node = heapq.heappop(self.h)
                if node not in self.visited:
                    break

            if node == self.end_node:
                return (self.distance[node], self._make_path())

            neighbors = self.get_neighbors(node)
            node_dist = self.distance[node]
            for neighbor in neighbors:
                if not neighbor in self.visited:
                    cost = self.get_cost(node, neighbor)
                    neighbor_dist = self.distance.get(neighbor)
                    new_dist = node_dist + cost
                    if neighbor_dist == None or new_dist < neighbor_dist:
                        self.distance[neighbor] = new_dist
                        heapq.heappush(self.h, (new_dist, neighbor))
                        self.back[neighbor] = node

    def _make_path(self):
        path = []
        node = self.end_node
        path.append(node)
        while node != self.start_node:
            node = self.back[node]
            path.append(node)
        path.reverse()
        return path

