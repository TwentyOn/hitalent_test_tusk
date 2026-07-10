import datetime

from sqlalchemy import Column, Integer, Text, String, DateTime, ARRAY, JSON

from backend.db import Base

class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True, autoincrement=True)
    rubrics = Column(ARRAY(String).with_variant(JSON, 'sqlite'))
    text = Column(Text)
    created_date = Column(DateTime, default=datetime.datetime.now)