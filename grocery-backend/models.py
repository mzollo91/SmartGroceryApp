from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True) # Index not needed as SQLAlchemy automatically creates an index for primary keys.
    # Indext used for faster lookups on non-primary key columns. Since 'id' is a primary key, it is already indexed.
    name = Column(String, nullable=False)

    aisles = relationship("Aisle", back_populates="store", cascade="all, delete-orphan")

class Aisle(Base):
    __tablename__ = "aisles"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    store_id = Column(Integer, ForeignKey("stores.id", ondelete="CASCADE"), nullable=False)

    store = relationship("Store", back_populates="aisles")

class Edge(Base):
    __tablename__ = "edges"

    id = Column(Integer, primary_key=True)
    aisle_a_id = Column(Integer, ForeignKey("aisles.id"), nullable=False)
    aisle_b_id = Column(Integer, ForeignKey("aisles.id"), nullable=False)

    aisle_a = relationship("Aisle", foreign_keys=[aisle_a_id])
    aisle_b = relationship("Aisle", foreign_keys=[aisle_b_id])
    distance = Column(Float, nullable=False)