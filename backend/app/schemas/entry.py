from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict, model_validator

from .analysis import AnalysisResultResponse


class EntryCreate(BaseModel):
    content: str
    title: Optional[str] = None
    category_id: Optional[UUID] = None
    user_tags: List[str] = []


class EntryUpdate(BaseModel):
    content: Optional[str] = None
    title: Optional[str] = None
    category_id: Optional[UUID] = None
    user_tags: Optional[List[str]] = None


class EntryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: Optional[str] = None
    content: str
    category_id: Optional[UUID] = None
    user_tags: List[str] = []
    analysis: Optional[AnalysisResultResponse] = None
    created_at: datetime
    updated_at: datetime

    @model_validator(mode="before")
    @classmethod
    def _build_from_orm(cls, data):
        if isinstance(data, dict):
            return data
        return {
            "id": data.id,
            "title": data.title,
            "content": data.content,
            "category_id": data.category_id,
            "user_tags": [t.tag_name for t in (data.tags or []) if t.tag_type == "user_defined"],
            "analysis": data.analysis_result,
            "created_at": data.created_at,
            "updated_at": data.updated_at,
        }


class EntryGroupedByMonth(BaseModel):
    month: str
    entries: List[EntryResponse]
