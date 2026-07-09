from fastapi import APIRouter, HTTPException, Response, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db import get_db
from backend.elastic import search_docs, delete_doc
from models import Document
from schemas import DocumentSchema

router = APIRouter(tags=['документы'])


@router.get('/documents', response_model=list[DocumentSchema], description='Поиск документов')
async def search_documents(query: str, db: AsyncSession = Depends(get_db)) -> list[DocumentSchema]:
    search_result = await search_docs(query)
    result = await db.execute(
        select(Document).
        where(Document.id.in_(search_result)).
        order_by(Document.created_date.desc())
    )
    documents = result.scalars().all()

    return documents


@router.delete("/documents/{id}", description='Удаление документа')
async def delete_document(pk: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Document).where(Document.id == pk)
    result = await db.scalars(stmt)
    db_document = result.first()

    if db_document is None:
        raise HTTPException(status_code=404, detail="Документ не найден")

    await db.delete(db_document)
    index_deleted = await delete_doc(pk)

    if not index_deleted:
        raise HTTPException(status_code=500, detail='Ошибка при удалении документа')

    await db.commit()

    return Response(status_code=204)
