from typing import List, Optional, Union
from uuid import UUID
from datetime import date

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..routers.auth import get_current_user
from ..schemas.entry import EntryCreate, EntryUpdate, EntryResponse, EntryGroupedByMonth
from ..schemas.analysis import AnalysisResultResponse
from ..services import entry_service, ai_service

router = APIRouter(prefix="/api/entries", tags=["Entries"])


@router.get("", response_model=Union[List[EntryGroupedByMonth], List[EntryResponse]])
def list_entries(
    grouped: bool = Query(False),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    category_id: Optional[UUID] = Query(None),
    tag: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if grouped:
        groups = entry_service.get_entries_grouped_by_month(
            db, current_user.id,
            date_from=date_from, date_to=date_to,
            category_id=category_id, tag=tag,
        )
        return [EntryGroupedByMonth(month=g["month"], entries=[EntryResponse.model_validate(e) for e in g["entries"]]) for g in groups]

    entries = entry_service.get_entries(
        db, current_user.id,
        page=page, limit=limit,
        date_from=date_from, date_to=date_to,
        category_id=category_id, tag=tag,
    )
    return [EntryResponse.model_validate(e) for e in entries]


@router.post("", response_model=EntryResponse, status_code=status.HTTP_201_CREATED)
def create_entry(
    data: EntryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    entry = entry_service.create_entry(db, current_user.id, data)
    return EntryResponse.model_validate(entry)


@router.get("/{entry_id}", response_model=EntryResponse)
def get_entry(
    entry_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    entry = entry_service.get_entry_by_id(db, current_user.id, entry_id)
    return EntryResponse.model_validate(entry)


@router.put("/{entry_id}", response_model=EntryResponse)
def update_entry(
    entry_id: UUID,
    data: EntryUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    entry = entry_service.update_entry(db, current_user.id, entry_id, data)
    return EntryResponse.model_validate(entry)


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_entry(
    entry_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    entry_service.delete_entry(db, current_user.id, entry_id)


@router.post("/{entry_id}/analyze", response_model=AnalysisResultResponse)
async def analyze_entry(
    entry_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Verify ownership first
    entry_service.get_entry_by_id(db, current_user.id, entry_id)
    result = await ai_service.analyze_entry(db, entry_id)
    return result


@router.get("/{entry_id}/analysis", response_model=Optional[AnalysisResultResponse])
def get_entry_analysis(
    entry_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    entry = entry_service.get_entry_by_id(db, current_user.id, entry_id)
    return entry.analysis_result
