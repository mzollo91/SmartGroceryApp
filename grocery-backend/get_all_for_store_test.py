"""Test script for get_all_for_store function."""

import asyncio
from database import AsyncSessionLocal
from DistanceRepository import DistanceRepository

async def print_edge_info():
    dr = DistanceRepository()
    try:
        async with AsyncSessionLocal() as session:
            edges = await dr.get_all_for_store(session=session, store_id=1) # Store ID verified using SQLite Viewer
            for edge in edges:
                print(f"Properties for Edge ID {edge.id}:")
                print(f"Aisle A ID: {edge.aisle_a_id}")
                print(f"Aisle B ID: {edge.aisle_b_id}")
                print(f"Distance (ft): {edge.distance}\n")
                
    except Exception as e:
        print(f"Error connecting to the database: {e}")

if __name__ == "__main__":
    asyncio.run(print_edge_info())