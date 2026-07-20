"""Test fixture for api calls."""

import pytest, pytest_asyncio
from test_db_schema import init_db
from test_db_seed_data import seed_test_data
from fastapi.testclient import TestClient
from main import app, get_session
from test_db_engine import AsyncSessionLocal, engine, Base # If I am importing initially here, all methods and functions are already stored in Python's cache. Importing engine, Base later in the code does not bring them in at that time.
from pathlib import Path

async def get_test_session():
    async with AsyncSessionLocal() as session:
        yield session

# Fixture ordering outline dependency ordering. A fixture with a dependency specified inherits the all of the upstream dependencies.
@pytest_asyncio.fixture(scope="session",loop_scope="session")
async def import_engine():
    # Database must be created first. Delete the original, if it exists.
    db_path = Path("test_grocery.db")
    db_path.unlink(missing_ok=True)

    # Only the engine object needs to be passed to the next fixture. A local session is created outside of the chain to align with FastAPI's injection method in the override_dependencies fixture.
    yield engine, Base

@pytest_asyncio.fixture(scope="session",loop_scope="session")
async def create_schema(import_engine):
    # Depends on engine being created.
    # Schema must created first by running the corresponding module.
    engine, Base = import_engine
    await init_db(engine=engine, Base=Base)
    yield

@pytest_asyncio.fixture(scope="session",loop_scope="session")
async def seed_data(create_schema):
    # Depends on the schema being created.
    # Seed data module is not currently idempotent (no duplicate error handling). Data must be seeded first.

    # Calling get_test_session() will yield an async generator object, not the actual async session. Instead of calling it here, mirror the body of get_test_session() within this fixture.
    async with AsyncSessionLocal() as session:
        await seed_test_data(session=session)
    yield

@pytest_asyncio.fixture(scope="session",loop_scope="session")
async def override_dependencies(seed_data):
    # Depends on the data being seeded
    app.dependency_overrides[get_session] = get_test_session
    yield # No value needed to be yielded, just a pause to allow the test fixture to run.
    app.dependency_overrides.clear() # or use app.dependency_overrides = {}

@pytest.fixture(scope="session")
def client(override_dependencies): # avoid 'test_' prefixes unless the function is a dedicated test function. Pytest's collection mechanism looks for this prefix to identify test functions.
    # Depends on the dependency override.
    with TestClient(app=app) as client:
        yield client
        # Test logic to follow...