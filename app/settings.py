import os
from pydantic import BaseModel

from dotenv import load_dotenv

load_dotenv()

class DbConfig(BaseModel):
    user: str = os.getenv("POSTGRES_USER")
    password: str = os.getenv("POSTGRES_PASSWORD")
    db_name: str = os.getenv("POSTGRES_DB")
    host: str = os.getenv("POSTGRES_HOST")
    port: int = os.getenv("POSTGRES_PORT")

    def get_db_url(self):
        return f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}'

class ElasticConfig(BaseModel):
    host: str = os.getenv("ELASTIC_HOST")
    api_key: str = os.getenv("ELASTIC_API_KEY")