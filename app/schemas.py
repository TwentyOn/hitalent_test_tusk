from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentSchema(BaseModel):
    id: int
    rubrics: list[str]
    text: str
    created_date: datetime

    model_config = ConfigDict(from_attributes=True)