from fastapi import APIRouter, HTTPException, Response, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db import get_db
from backend.elastic import ElasticClient
from models import Document
from schemas import DocumentSchema

router = APIRouter(tags=['документы'])


@router.get('/documents', response_model=list[DocumentSchema], description='Поиск документов')
async def search_documents(query: str, db: AsyncSession = Depends(get_db)) -> list[DocumentSchema]:
    elastic_client = ElasticClient()
    try:
        search_result = await elastic_client.search_docs(query)
        result = await db.execute(
            select(Document).
            where(Document.id.in_(search_result)).
            order_by(Document.created_date.desc())
        )
        documents = result.scalars().all()

        return documents
    finally:
        await elastic_client.close_client()


@router.delete("/documents/{pk}", description='Удаление документа')
async def delete_document(pk: int, db: AsyncSession = Depends(get_db)):
    elastic_client = ElasticClient()
    try:
        stmt = select(Document).where(Document.id == pk)
        result = await db.scalars(stmt)
        db_document = result.first()

        if db_document is None:
            raise HTTPException(status_code=404, detail="Документ не найден")

        await db.delete(db_document)
        index_deleted = await elastic_client.delete_doc(pk)

        if not index_deleted:
            raise HTTPException(status_code=500, detail='Ошибка при удалении документа')

        await db.commit()

        return Response(status_code=204)
    finally:
        await elastic_client.close_client()
