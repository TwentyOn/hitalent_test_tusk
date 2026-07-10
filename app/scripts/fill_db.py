import csv
import datetime
import logging

from sqlalchemy import insert

from models import Document
from backend.db import async_session_maker

logging.basicConfig(level=logging.INFO, format='[{asctime}] #{levelname:4} {name}:{lineno} - {message}', style='{')
logger = logging.getLogger(__name__)


async def fill_db():
    try:
        logger.info('Заполнение БД...')

        with open('scripts/posts.csv', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            async with async_session_maker() as session:
                for row in reader:
                    row['created_date'] = datetime.datetime.fromisoformat(row['created_date'])
                    row['rubrics'] = eval(row['rubrics'])
                    await session.execute(insert(Document).values(**row))

                await session.commit()

        logger.info('БД успешно заполнена')
    except Exception as e:
        logger.info('Ошибка заполнения БД', exc_info=True)
