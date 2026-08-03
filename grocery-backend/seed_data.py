"""Small script to seed initial date into grocery.db"""
import asyncio
from database import AsyncSessionLocal
from models import Store, Aisle, Edge

async def seed():
    async with AsyncSessionLocal() as session:
        store = Store(name="Giant")
        session.add(store)
        await session.flush() # Complete transaction without ending session.

        entrance = Aisle(name="Entrance", store_id=store.id)
        produce = Aisle(name="Produce", store_id=store.id)
        dairy = Aisle(name="Dairy", store_id=store.id)
        checkout = Aisle(name="Checkout", store_id=store.id)
        session.add_all([entrance, produce, dairy, checkout])
        await session.flush()  # assigns ids to each aisle
        
        edges = [
            Edge(aisle_a_id=entrance.id, aisle_b_id=produce.id, distance=5.0),
            Edge(aisle_a_id=produce.id, aisle_b_id=dairy.id, distance=3.0),
            Edge(aisle_a_id=dairy.id, aisle_b_id=checkout.id, distance=4.0),
        ]
        session.add_all(edges)

        store = Store(name="Walmart")
        session.add(store)
        await session.flush() # Complete transaction without ending session.

        entrance = Aisle(name="Entrance", store_id=store.id)
        produce = Aisle(name="Produce", store_id=store.id)
        dairy = Aisle(name="Dairy", store_id=store.id)
        checkout = Aisle(name="Checkout", store_id=store.id)
        session.add_all([entrance, produce, dairy, checkout])
        await session.flush()  # assigns ids to each aisle
        
        edges = [
            Edge(aisle_a_id=entrance.id, aisle_b_id=produce.id, distance=7.0),
            Edge(aisle_a_id=produce.id, aisle_b_id=dairy.id, distance=10.0),
            Edge(aisle_a_id=dairy.id, aisle_b_id=checkout.id, distance=3.0),
        ]
        session.add_all(edges)

        await session.commit()
        print(f"Seeded store_id={store.id} with 4 aisles and 3 edges.")

if __name__ == "__main__":
    asyncio.run(seed())