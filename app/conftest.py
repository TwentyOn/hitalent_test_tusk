from unittest.mock import patch

import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from elasticsearch import AsyncElasticsearch

from backend import elastic
from backend.db import Base, get_db
from backend.elastic import get_client
import backend.elastic
from models import Document
from settings import ElasticConfig
from scripts.fill_index import bulk_data
from scripts.fill_db import fill_db
from main import app
from routers.documents import INDEX_NAME

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


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

__is_filled = False
@pytest_asyncio.fixture(scope="session")
async def app_test(async_sessionmaker):
    async def _get_db():
        global __is_filled
        async with async_sessionmaker() as session:
            try:
                if not __is_filled:
                    __is_filled = True
                    await fill_db(session)

                with (
                    patch('scripts.fill_index.INDEX_NAME', 'test_documents'),
                ):
                    await bulk_data(session)
                yield session
            finally:
                await session.rollback()

    es_conf = ElasticConfig()
    client = AsyncElasticsearch(
        es_conf.host,
        request_timeout=30,
        api_key=es_conf.api_key,
    )

    async def _get_client():
        return client

    app.dependency_overrides[get_db] = _get_db
    # app.dependency_overrides[get_client] = _get_client
    yield app
    app.dependency_overrides.clear()

@pytest_asyncio.fixture(scope="session")
async def client(app_test: FastAPI):
    with TestClient(app=app_test) as client:
        yield client
