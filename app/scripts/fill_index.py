import asyncio

from elasticsearch import helpers
from sqlalchemy import select

from backend.db import async_session_maker
from models import Document
from backend.elastic import client


async def generate_docs(docs):
    for row in docs:
        i = row['id']
        yield {
            "_index": "documents",
            "_id": i,
            "id": i,
            "text": row['text'],
        }


async def bulk_data():
    async with async_session_maker() as session:
        result = await session.execute(select(Document.id, Document.text))
        documents = result.mappings().all()

    await helpers.async_bulk(client, generate_docs(documents))


asyncio.run(bulk_data())
