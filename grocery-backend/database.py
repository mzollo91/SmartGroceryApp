from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import event
from sqlalchemy.engine import Engine
from dotenv import load_dotenv
import os

# DATABASE_URL = "sqlite+aiosqlite:///./grocery.db"
load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]

# Base is the parent class that every table model will inherit from.
# It provides the necessary metadata and functionality for SQLAlchemy to work with the database.

engine = create_async_engine(DATABASE_URL, echo=True)

@event.listens_for(engine.sync_engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

Base = declarative_base()

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

async def get_db():
    """FastAPI dependency: yields a session and guarantees cleanup."""
    async with AsyncSessionLocal() as session:
        yield session