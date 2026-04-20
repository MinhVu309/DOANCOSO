from typing import List
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status

from ..models.category import Category
from ..models.entry import Entry
from ..schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse


def get_categories(db: Session, user_id: int) -> List[CategoryResponse]:
    rows = (
        db.query(Category, func.count(Entry.id).label("entry_count"))
        .outerjoin(Entry, Entry.category_id == Category.id)
        .filter(Category.user_id == user_id)
        .group_by(Category.id)
        .order_by(Category.created_at)
        .all()
    )
    result = []
    for cat, count in rows:
        resp = CategoryResponse(
            id=cat.id,
            name=cat.name,
            icon=cat.icon,
            color_theme=cat.color_theme,
            entry_count=count,
        )
        result.append(resp)
    return result


def get_category_by_id(db: Session, user_id: int, category_id: UUID) -> Category:
    cat = db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == user_id,
    ).first()
    if cat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy danh mục")
    return cat


def create_category(db: Session, user_id: int, data: CategoryCreate) -> Category:
    cat = Category(user_id=user_id, name=data.name, icon=data.icon, color_theme=data.color_theme)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


def update_category(db: Session, user_id: int, category_id: UUID, data: CategoryUpdate) -> Category:
    cat = get_category_by_id(db, user_id, category_id)
    if data.name is not None:
        cat.name = data.name
    if data.icon is not None:
        cat.icon = data.icon
    if data.color_theme is not None:
        cat.color_theme = data.color_theme
    db.commit()
    db.refresh(cat)
    return cat


def delete_category(db: Session, user_id: int, category_id: UUID) -> None:
    cat = get_category_by_id(db, user_id, category_id)
    # Null-out entries that reference this category
    db.query(Entry).filter(Entry.category_id == category_id).update({"category_id": None})
    db.delete(cat)
    db.commit()
