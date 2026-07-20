"""Test fixture for api calls."""

import pytest, pytest_asyncio
from test_db_schema import init_db
from test_db_seed_data import seed_test_data
from fastapi.testclient import TestClient
from main import app, get_session
from test_db_engine import get_db, AsyncSessionLocal

async def get_test_session():
    async with AsyncSessionLocal() as session:
        yield session

# Fixture ordering outline dependency ordering. A fixture with a dependency specified inherits the all of the upstream dependencies.
@pytest_asyncio.fixture
async def engine():
    # Database must be created first.
    get_test_session = get_db()
    yield get_test_session
    # Closing the session should not be needed, get_db() uses a 'with' block and yields a session when run. This should close the session automatically at the end of the test.

@pytest_asyncio.fixture
async def create_schema(engine):
    # Depends on engine being created.
    # Schema must created first by running the corresponding module.
    get_test_session = engine
    yield get_test_session

@pytest_asyncio.fixture
async def seed_data(create_schema):
    # Depends on the schema being created.
    # Seed data module is not currently idempotent (no duplicate error handling). Data must be seeded first.
    get_test_session = create_schema
    yield get_test_session

@pytest_asyncio.fixture
async def override_dependencies(seed_data):
    # Depends on the data being seeded
    get_test_session = engine
    app.dependency_overrides[get_session] = get_test_session
    yield # No value needed to be yielded, just a pause to allow the test fixture to run.
    app.dependency_overrides.clear() # or use app.dependency_overrides = {}

@pytest.fixture
def client(override_dependencies): # avoid 'test_' prefixes unless the function is a dedicated test function. Pytest's collection mechanism looks for this prefix to identify test functions.
    # Depends on the dependency override.
    with TestClient(app=app) as client:
        yield client
        # Test logic to follow...