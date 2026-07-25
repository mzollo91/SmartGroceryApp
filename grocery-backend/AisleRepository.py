"""Repo for interacting with the 'aisle' table in the database."""

from sqlalchemy import select
from models import Aisle

class AisleRepository:

    async def get_all_aisles_in_store(self, session, store_id):
        # Pull all aisle IDs for a given store.
        statement = select(Aisle).where(Aisle.store_id == store_id)
        result = await session.execute(statement)
        aisles = result.scalars().all()

        return aisles
    
    async def get_aisle(self, session, aisle_id):
        # Get a single aisle by ID.
        statement = select(Aisle).where(Aisle.id == aisle_id)
        result = await session.execute(statement)
        aisle = result.scalar_one_or_none()

        return aisle