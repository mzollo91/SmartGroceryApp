from collections import defaultdict
import heapq

from networkx import predecessor

class Pathfinder:
    def __init__(self, db_manager):
        self.db = db_manager
        self.adj_list = defaultdict(list)

    def refresh_graph(self):
        # Fetches all distances to build adjaceny list.
        distances = self.db.get_all_distances()

        # Clear the old graph if it exists.
        self.adj_list = defaultdict(list)
    
        for dist in distances:
            self.adj_list[dist.store_a_name].append((dist.store_b_name,dist.travel_distance_minutes))

        return self.adj_list

    def reconstruct_path(self, predeccors, start_node, end_node):
        """
        Traces back from the end_node to the start_node using the predecessors dictionary, then reverses it for the user.
        """
        
        path = []
        current = end_node
        # Backtrack: End -> Start
        while current is not None:
            path.append(current)
            if current == start_node:
                break
            current = predeccors.get(current)

        # Validation: If the last node isn''t the start , there's no path.
        if not path or path[-1] != start_node:
            return []

        # Reverse to get Start -> End
        return path[::-1]

    def find_shortest_path(self, start_node, end_node):
        """
        Djykstra's algorithm to find the shortest path between two nodes in a graph.
        This translates to finding the shortest travel time between two stores based on the distances in the database.
        Returns a tuple.
        """

        # Refresh the graph from the DB to ensure we have the latest distances.
        adj_list = self.refresh_graph()

        # Priority queue: stores tuples of (cumulative_minutes, current_node)
        # Python min-heaps sort by the first element of the tuple automatically.

        pq = [(0, start_node)]

        # Creating some bookeeping structures:
        distances = {start_node: 0}
        predecessors = {start_node: None}
        visited = set()

        # The core djykstra's loop:

        while pq:
            current_time, current_node = heapq.heappop(pq)
            # If we pooped the destination, we can stop and reconstruct the path.
            if current_node == end_node:
                break
            # If we've already finalized this node, skip it.
            if current_node in visited:
                continue

            visited.add(current_node)

            # Explore the neighbors of the current node:
            for neighbor, travel_time in adj_list[current_node]:
                if neighbor in visited:
                    continue

                # Calculate the new cumulative time to reach this neighbor through the current node.
                new_time = current_time + travel_time

                # Relaxtion step: if this path to the neighbor is better, update our structures.
                if neighbor not in distances or new_time < distances[neighbor]:
                    distances[neighbor] = new_time
                    predecessors[neighbor] = current_node # Leave a breadcrumb.
                    heapq.heappush(pq, (new_time, neighbor))

            # Path reconstruction and output:
            path = self.reconstruct_path(predecessors, start_node, end_node)
            total_time = distances.get(end_node, float('inf'))

            # If the destination is unreachable, return an empty path and infinite cost.
            if total_time == float('inf'):
                return [], float('inf')

            return path, total_time
                


