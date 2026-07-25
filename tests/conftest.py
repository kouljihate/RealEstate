import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from backend.core.config import get_settings
from backend.core.database import Database


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def db() -> AsyncGenerator:
    settings = get_settings()
    test_uri = settings.MONGODB_URI
    test_db = f"{settings.MONGODB_DB}_test"
    await Database.connect(test_uri, test_db)
    yield Database.get_db()
    client = Database.client
    if client:
        await client.drop_database(test_db)
    await Database.close()


@pytest_asyncio.fixture(scope="function")
async def clean_db(db):
    collections = await db.list_collection_names()
    for col in collections:
        await db[col].delete_many({})
    yield db


@pytest_asyncio.fixture
async def client() -> AsyncGenerator:
    from backend.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
