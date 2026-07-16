"""A simple test script to test the pathfinder module against seeded data."""

import asyncio
from database import AsyncSessionLocal
from DistanceRepository import DistanceRepository
from Pathfinder import Pathfinder

async def find_shortest_path_test():
    dr = DistanceRepository()
    pf = Pathfinder(distance_repo=dr)
    try:
        async with AsyncSessionLocal() as session:
            start_node_id = 1 # Entrance ID in the database
            end_node_id = 1 # Checkout ID in the database
            store_id = 1 # Currently only store in the database

            path, total_distance = await pf.find_shortest_path(start_node_id=start_node_id, end_node_id=end_node_id, session=session, store_id=store_id)

            return path, total_distance


    except Exception as e:
        print(f"Error connecting to the database: {e}")

if __name__ == "__main__":
    result = asyncio.run(find_shortest_path_test())
    if result is not None:
        total_nodes = len(result[0])
        for index, edge in enumerate(result[0]):
            if index == total_nodes - 1:
                print(f"ID: {edge}")
            else:
                print(f"ID: {edge} ->")
        print(f"Total distance (ft): {result[1]}")