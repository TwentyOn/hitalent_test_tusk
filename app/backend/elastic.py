import logging

from elasticsearch import AsyncElasticsearch

from settings import ElasticConfig

logger = logging.getLogger(__name__)
config = ElasticConfig()
INDEX_NAME = 'documents'

client = AsyncElasticsearch(
    config.host,
    request_timeout=30,
    api_key=config.api_key,
)


def get_client() -> AsyncElasticsearch:
    return client
