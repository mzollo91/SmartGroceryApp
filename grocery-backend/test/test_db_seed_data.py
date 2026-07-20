"""Module to seed data for the test db."""
import asyncio
#from test_db_engine import AsyncSessionLocal
from models import Store, Aisle, Edge

async def seed_test_data(session):

    store_a = Store(name="Giant")
    session.add(store_a)
    await session.flush() # Complete transaction without ending session.

    entrance_a = Aisle(name="Entrance", store_id=store_a.id)
    produce_a = Aisle(name="Produce", store_id=store_a.id)
    dairy_a = Aisle(name="Dairy", store_id=store_a.id)
    checkout_a = Aisle(name="Checkout", store_id=store_a.id)

    session.add_all([entrance_a, produce_a, dairy_a, checkout_a])
    await session.flush()  # assigns ids to each aisle
    
    # Create edges with one isolated aisle that has no path to it.
    edges_a = [
        Edge(aisle_a_id=entrance_a.id, aisle_b_id=produce_a.id, distance=5.0),
        Edge(aisle_a_id=produce_a.id, aisle_b_id=checkout_a.id, distance=3.0),
        Edge(aisle_a_id=entrance_a.id, aisle_b_id=checkout_a.id, distance=4.0),
    ]
    session.add_all(edges_a)

    store_b = Store(name="Walmart")
    session.add(store_b)
    await session.flush() # Complete transaction without ending session.

    entrance_b = Aisle(name="Entrance", store_id=store_b.id)
    checkout_b = Aisle(name="Checkout", store_id=store_b.id)

    session.add_all([entrance_b, checkout_b])
    await session.flush()  # assigns ids to each aisle

    edges_b = [
        Edge(aisle_a_id=entrance_b.id, aisle_b_id=checkout_b.id, distance=10.0),
    ]

    await session.commit()
    print(f"Seeded store '{store_a.name}' with 4 aisles (1 isolated) and 3 edges.")
    print(f"Seeded store '{store_b.name}' with 2 aisles and 1 edge.")

#if __name__ == "__main__":
#    asyncio.run(seed_test_data())