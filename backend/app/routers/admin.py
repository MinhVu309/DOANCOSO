from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..models.user import User
from ..routers.auth import get_current_admin
from ..schemas.admin import (
    PlatformStatsResponse,
    AdminUserListResponse,
    AdminToggleActiveResponse,
)
from ..services.admin_service import (
    get_platform_stats,
    list_all_users,
    toggle_user_active,
)

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/stats", response_model=PlatformStatsResponse)
def admin_stats(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    return get_platform_stats(db)


@router.get("/users", response_model=AdminUserListResponse)
def admin_list_users(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    return list_all_users(db, page=page, limit=limit, search=search)


@router.patch("/users/{user_id}/toggle-active", response_model=AdminToggleActiveResponse)
def admin_toggle_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    return toggle_user_active(db, user_id=user_id, current_admin_id=current_admin.id)
