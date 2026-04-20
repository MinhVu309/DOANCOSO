from typing import List, Optional
from uuid import UUID
from datetime import date
from collections import defaultdict

from sqlalchemy.orm import Session, selectinload
from sqlalchemy import and_
from fastapi import HTTPException, status

from ..models.entry import Entry
from ..models.entry_tag import EntryTag
from ..schemas.entry import EntryCreate, EntryUpdate


def _base_query(db: Session, user_id: int):
    return (
        db.query(Entry)
        .options(
            selectinload(Entry.tags),
            selectinload(Entry.analysis_result),
        )
        .filter(Entry.user_id == user_id)
    )


def get_entry_by_id(db: Session, user_id: int, entry_id: UUID) -> Entry:
    entry = _base_query(db, user_id).filter(Entry.id == entry_id).first()
    if entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy nhật ký")
    return entry


def get_entries(
    db: Session,
    user_id: int,
    page: int = 1,
    limit: int = 20,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    category_id: Optional[UUID] = None,
    tag: Optional[str] = None,
) -> List[Entry]:
    q = _base_query(db, user_id)

    if date_from:
        q = q.filter(Entry.created_at >= date_from)
    if date_to:
        q = q.filter(Entry.created_at <= date_to)
    if category_id:
        q = q.filter(Entry.category_id == category_id)
    if tag:
        q = q.join(Entry.tags).filter(
            and_(EntryTag.tag_name == tag, EntryTag.tag_type == "user_defined")
        )

    return q.order_by(Entry.created_at.desc()).offset((page - 1) * limit).limit(limit).all()


def get_entries_grouped_by_month(
    db: Session,
    user_id: int,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    category_id: Optional[UUID] = None,
    tag: Optional[str] = None,
) -> List[dict]:
    """Group entries by month for the History page."""
    entries = get_entries(
        db, user_id,
        page=1, limit=1000,
        date_from=date_from, date_to=date_to,
        category_id=category_id, tag=tag,
    )

    grouped: dict = defaultdict(list)
    for entry in entries:
        if entry.created_at:
            key = entry.created_at.strftime("%B %Y")  # e.g. "April 2026"
        else:
            key = "Unknown"
        grouped[key].append(entry)

    result = [{"month": month, "entries": items} for month, items in grouped.items()]
    return result


def create_entry(db: Session, user_id: int, data: EntryCreate) -> Entry:
    entry = Entry(
        user_id=user_id,
        title=data.title,
        content=data.content,
        category_id=data.category_id,
    )
    db.add(entry)
    db.flush()  # get entry.id without committing

    for tag_name in data.user_tags:
        tag = EntryTag(entry_id=entry.id, tag_name=tag_name, tag_type="user_defined")
        db.add(tag)

    db.commit()
    db.refresh(entry)
    # Reload with relationships
    return get_entry_by_id(db, user_id, entry.id)


def update_entry(db: Session, user_id: int, entry_id: UUID, data: EntryUpdate) -> Entry:
    entry = get_entry_by_id(db, user_id, entry_id)

    if data.content is not None:
        entry.content = data.content
    if data.title is not None:
        entry.title = data.title
    if data.category_id is not None:
        entry.category_id = data.category_id

    if data.user_tags is not None:
        # Sync user_defined tags
        db.query(EntryTag).filter(
            EntryTag.entry_id == entry_id,
            EntryTag.tag_type == "user_defined"
        ).delete()
        for tag_name in data.user_tags:
            db.add(EntryTag(entry_id=entry_id, tag_name=tag_name, tag_type="user_defined"))

    db.commit()
    db.refresh(entry)
    return get_entry_by_id(db, user_id, entry_id)


def delete_entry(db: Session, user_id: int, entry_id: UUID) -> None:
    entry = get_entry_by_id(db, user_id, entry_id)
    db.delete(entry)
    db.commit()
