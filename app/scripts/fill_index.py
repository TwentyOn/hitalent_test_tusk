import logging

from elasticsearch import helpers
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Document
from backend.db import async_session_maker
from backend.elastic import client, INDEX_NAME

logging.basicConfig(level=logging.INFO, format='[{asctime}] #{levelname:4} {name}:{lineno} - {message}', style='{')
logger = logging.getLogger(__name__)


async def generate_docs(docs):
    for row in docs:
        i = row['id']
        yield {
            "_index": INDEX_NAME,
            "_id": i,
            "id": i,
            "text": row['text'],
        }


async def bulk_data(session: AsyncSession | None = None):
    try:
        if await client.indices.exists(index=INDEX_NAME):
            logger.info('Удаление существующего индекса...')
            await client.indices.delete(index=INDEX_NAME)

        logger.info('Заполнение индекса...')
        if session is None:
            async with async_session_maker() as session:
                result = await session.execute(select(Document.id, Document.text))
        else:
            result = await session.execute(select(Document.id, Document.text))

        documents = result.mappings().all()

        await helpers.async_bulk(client, generate_docs(documents))
        logger.info('Индекс успешно заполнен')
    except Exception as e:
        logger.error('Ошибка заполнения идекса', exc_info=True)
