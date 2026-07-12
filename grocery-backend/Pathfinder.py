from collections import defaultdict
import heapq

class Pathfinder:
    def __init__(self, distance_repo):
        self.dr = distance_repo
        self.adj_list = defaultdict(list)

    async def refresh_graph(self, session, store_id):
        """Fetches all distances to build adjaceny list."""
        edges = await self.dr.get_all_for_store(session=session, store_id=store_id)

        # Clear the old graph if it exists.
        self.adj_list = defaultdict(list)
    
        for edge in edges:
            self.adj_list[edge.aisle_a_id].append((edge.aisle_b_id,edge.distance))
            self.adj_list[edge.aisle_b_id].append((edge.aisle_a_id,edge.distance))

        return self.adj_list

    def reconstruct_path(self, predecessors, start_node_id, end_node_id):
        """
        Traces back from the end_node_id to the start_node_id using the predecessors dictionary, then reverses it for the user.
        """
        
        path = []
        current = end_node_id
        # Backtrack: End -> Start
        while current is not None:
            path.append(current)
            if current == start_node_id:
                break
            current = predecessors.get(current)

        # Validation: If the last node isn't the start , there's no path.
        if not path or path[-1] != start_node_id:
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