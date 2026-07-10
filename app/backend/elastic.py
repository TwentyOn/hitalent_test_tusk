import logging

from elasticsearch import AsyncElasticsearch, NotFoundError

from settings import ElasticConfig

logger = logging.getLogger(__name__)
config = ElasticConfig()

INDEX_NAME = 'documents'

client = AsyncElasticsearch(
    config.host,
    request_timeout=30,
    api_key=config.api_key,
)


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
