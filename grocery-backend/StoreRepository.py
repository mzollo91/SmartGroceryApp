"""Repo for interacting with the 'store' table in the database."""

from sqlalchemy import select
from models import Store

class StoreRepository:

    async def get_all_stores(self, session):
        # Pull all store IDs available in the database.
        statement = select(Store)
        result = await session.execute(statement)
        stores = result.scalars().all()

        return stores
    
    async def get_store(self, session, store_id):
        # Get a single store by ID.
        statement = select(Store).where(Store.id == store_id)
        result = await session.execute(statement)
        store = result.scalar_one_or_none()

        return store