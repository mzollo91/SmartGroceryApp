from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./grocery.db"

# Base is the parent class that every table model will inherit from.
# It provides the necessary metadata and functionality for SQLAlchemy to work with the database.

engine = create_async_engine(DATABASE_URL, echo=True)

Base = declarative_base()

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

async def get_db():
    """FastAPI dependency: yields a session and guarantees cleanup."""
    async with AsyncSessionLocal() as session:
        yield session