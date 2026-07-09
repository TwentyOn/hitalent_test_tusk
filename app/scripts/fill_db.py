import csv
import asyncio
import datetime

from sqlalchemy import insert

from models import Document
from backend.db import async_session_maker


async def fill_db():
    with open('posts.csv', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        async with async_session_maker() as session:
            for row in reader:
                row['created_date'] = datetime.datetime.fromisoformat(row['created_date'])
                row['rubrics'] = eval(row['rubrics'])
                await session.execute(insert(Document).values(**row))

            await session.commit()


asyncio.run(fill_db())
