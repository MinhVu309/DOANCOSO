from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class CategoryCreate(BaseModel):
    name: str
    icon: str = "folder"
    color_theme: str = "#6B7355"


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    icon: Optional[str] = None
    color_theme: Optional[str] = None


class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    icon: str
    color_theme: str
    entry_count: int = 0
