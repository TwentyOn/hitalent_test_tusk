import asyncio

from scripts.fill_db import fill_db
from scripts.fill_index import bulk_data

async def startup():
    await fill_db()
    await bulk_data()

asyncio.run(startup())
