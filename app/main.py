import logging

from fastapi import FastAPI

from routers import documents

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(documents.router)

