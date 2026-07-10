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

def get_client() -> AsyncElasticsearch:
    return client


# async def search_docs(index_name: str, query: str) -> list[int]:
#     docs = await get_client().search(
#         index=index_name,
#         query={
#             "match": {
#                 'text': query
#             }
#         },
#         size=20
#     )
#     ids = [d['_source']['id'] for d in docs['hits']['hits']]
#     return ids


# async def delete_doc(index_name: str, pk: int) -> bool:
#     try:
#         resp = await get_client().delete(index=index_name, id=str(pk))
#         return True if resp.get('result') == 'deleted' else False
#     except NotFoundError:
#         logger.error('Не удалось найти документ в индексе ElasticSearch', exc_info=True)
#         return False
#     except Exception as err:
#         logger.error('Не удалось удалить документ в индексе ElasticSearch', exc_info=True)
#         return False
