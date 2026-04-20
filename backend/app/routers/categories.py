from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..routers.auth import get_current_user
from ..schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from ..services import category_service

router = APIRouter(prefix="/api/categories", tags=["Categories"])


@router.get("", response_model=List[CategoryResponse])
def list_categories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return category_service.get_categories(db, current_user.id)


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    data: CategoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    cat = category_service.create_category(db, current_user.id, data)
    return CategoryResponse(id=cat.id, name=cat.name, icon=cat.icon, color_theme=cat.color_theme, entry_count=0)


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: UUID,
    data: CategoryUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    cat = category_service.update_category(db, current_user.id, category_id, data)
    # Re-fetch with count
    cats = category_service.get_categories(db, current_user.id)
    for c in cats:
        if c.id == cat.id:
            return c
    return CategoryResponse(id=cat.id, name=cat.name, icon=cat.icon, color_theme=cat.color_theme, entry_count=0)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    category_service.delete_category(db, current_user.id, category_id)
