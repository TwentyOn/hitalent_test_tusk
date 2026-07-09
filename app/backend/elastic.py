import asyncio
import logging

from elasticsearch import AsyncElasticsearch, NotFoundError

from settings import ELASTIC_API_KEY

INDEX_NAME = "documents"

logger = logging.getLogger(__name__)

client = AsyncElasticsearch(
    "https://my-elasticsearch-project-fdb0a9.es.us-central1.gcp.elastic.cloud:443",
    request_timeout=30,
    api_key=ELASTIC_API_KEY,
)


async def create_doc(document: dict) -> dict:
    resp = client.index(index=INDEX_NAME, id=str(document['id']), body=document)
    return resp.get('result')


async def search_docs(query: str) -> list[int]:
    docs = await client.search(
        index=INDEX_NAME,
        query={
            "match": {
                'text': query
            }
        },
        size=20
    )
    ids = [d['_source']['id'] for d in docs['hits']['hits']]
    return ids


async def delete_doc(pk: int) -> bool:
    try:
        resp = await client.delete(index=INDEX_NAME, id=str(pk))
        return True if resp.get('result') == 'deleted' else False
    except NotFoundError:
        logger.error('Не удалось найти документ в индексе ElasticSearch', exc_info=True)
        return False
    except Exception as err:
        logger.error('Не удалось удалить документ в индексе ElasticSearch', exc_info=True)
        return False
