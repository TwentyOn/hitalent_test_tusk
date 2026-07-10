import logging

from fastapi import APIRouter, HTTPException, Response, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from elasticsearch import Elasticsearch, NotFoundError

from backend.db import get_db
from backend.elastic import get_client, INDEX_NAME
from models import Document
from schemas import DocumentSchema


logger = logging.getLogger(__name__)
router = APIRouter(tags=['документы'])



@router.get('/documents', response_model=list[DocumentSchema], description='Поиск документов')
async def search_documents(
        query: str,
        db: AsyncSession = Depends(get_db),
        es: Elasticsearch = Depends(get_client)
) -> list[DocumentSchema]:

    docs = await es.search(
        index=INDEX_NAME,
        query={
            "match": {
                'text': query
            }
        },
        size=20
    )
    docs_ids = [d['_source']['id'] for d in docs['hits']['hits']]

    result = await db.execute(
        select(Document).
        where(Document.id.in_(docs_ids)).
        order_by(Document.created_date.desc())
    )
    documents = result.scalars().all()

    return documents


@router.delete("/documents/{pk}", description='Удаление документа')
async def delete_document(
        pk: int,
        db: AsyncSession = Depends(get_db),
        es: Elasticsearch = Depends(get_client)
):
    stmt = select(Document).where(Document.id == pk)
    result = await db.scalars(stmt)
    db_document = result.first()

    if db_document is None:
        raise HTTPException(status_code=404, detail="Документ не найден")

    await db.delete(db_document)

    try:
        await get_client().delete(index=INDEX_NAME, id=str(pk))
    except NotFoundError:
        raise HTTPException(status_code=404, detail='Не удалось найти документ')
    except Exception as err:
        logger.error('Не удалось удалить документ в индексе ElasticSearch', exc_info=True)
        raise HTTPException(status_code=500, detail='Не удалось удалить документ в индексе')


    await db.commit()

    return Response(status_code=204)
