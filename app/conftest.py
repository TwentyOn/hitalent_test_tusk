from unittest.mock import patch

import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from httpx2 import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from backend.db import Base, get_db
from backend.elastic import get_client
from scripts.fill_index import bulk_data
from scripts.fill_db import fill_db
from main import app
from settings import ElasticConfig

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
config = ElasticConfig()


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def async_sessionmaker(test_engine):
    return sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

@pytest_asyncio.fixture(scope="session")
async def app_test(async_sessionmaker):
    async def _get_db():
        async with async_sessionmaker() as session:
            try:
                yield session
            finally:
                await session.rollback()


    app.dependency_overrides[get_db] = _get_db

    app.dependency_overrides[get_client] = lambda: AsyncElasticsearch(
        config.host,
        request_timeout=30,
        api_key=config.api_key,
    )
    yield app
    app.dependency_overrides.clear()

@pytest_asyncio.fixture(scope="session")
async def fill_data(async_sessionmaker):
    client = AsyncElasticsearch(
        config.host,
        request_timeout=30,
        api_key=config.api_key,
    )
    async with async_sessionmaker() as session:
        await fill_db(session)
        with patch('scripts.fill_index.INDEX_NAME', 'test_documents'):
            await bulk_data(session)
    yield
    if await client.indices.exists(index='test_documents'):
        await client.indices.delete(index='test_documents')


@pytest_asyncio.fixture(scope='session')
async def client(app_test: FastAPI):
    transport = ASGITransport(app=app_test)
    async with AsyncClient(transport=transport, base_url="http://testserver") as c:
        yield c