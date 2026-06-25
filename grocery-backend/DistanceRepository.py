"""Repo for interacting with the 'edges' table in the database."""

from database import engine
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from models import Edge, Aisle

class DistanceRepo:
    # def __init__(self, session: AsyncSession):
    #     """Establish the async session upon initialization"""
    #     self.session = session

    async def get_all_for_store(self, session, store_id):
        # Pull the aisle IDs for a given store.
        statement = select(Aisle.id).where(Aisle.store_id == store_id)
        result = await session.execute(statement)
        aisle_ids = result.scalars().all()

        statement = select(Edge).where(or_(
            Edge.aisle_a_id.in_(aisle_ids),
            Edge.aisle_b_id.in_(aisle_ids)
            ))
        result = await session.execute(statement)
        edges = result.scalars().all()

        return edges
