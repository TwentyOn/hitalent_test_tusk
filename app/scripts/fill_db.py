import csv
import datetime
import logging
import os

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from models import Document
from backend.db import async_session_maker

logging.basicConfig(level=logging.INFO, format='[{asctime}] #{levelname:4} {name}:{lineno} - {message}', style='{')
logger = logging.getLogger(__name__)

def get_path() -> str | None:
    paths = ['app/scripts/posts.csv', 'posts.csv', 'scripts/posts.csv']
    for path in paths:
        if os.path.exists(path):
            return path
    return None


async def insert_data(session: AsyncSession):
    path = get_path()

    if not path:
        logger.error('Не найден csv файл')
        return

    with open(path, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['created_date'] = datetime.datetime.fromisoformat(row['created_date'])
            row['rubrics'] = eval(row['rubrics'])
            await session.execute(insert(Document).values(**row))

        await session.commit()
        logger.info('БД успешно заполнена')


async def fill_db(session: AsyncSession | None = None):
    try:
        logger.info('Заполнение БД...')

        if session is None:
            async with async_session_maker() as session:
                await insert_data(session)
        else:
            await insert_data(session)

    except Exception as e:
        logger.info('Ошибка заполнения БД', exc_info=True)
