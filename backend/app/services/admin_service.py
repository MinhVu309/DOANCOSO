from datetime import datetime, timezone, timedelta
from typing import Optional
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models.user import User
from ..models.entry import Entry
from ..models.analysis_result import AnalysisResult
from ..schemas.admin import (
    PlatformStatsResponse,
    AdminUserItem,
    AdminUserListResponse,
    AdminToggleActiveResponse,
)


def get_platform_stats(db: Session) -> PlatformStatsResponse:
    now = datetime.now(timezone.utc)
    week_ago = now - timedelta(days=7)

    total_users = db.query(func.count(User.id)).scalar()
    active_users = db.query(func.count(User.id)).filter(User.is_active == True).scalar()
    total_entries = db.query(func.count(Entry.id)).scalar()
    total_analyses = db.query(func.count(AnalysisResult.id)).scalar()
    new_users_this_week = (
        db.query(func.count(User.id)).filter(User.created_at >= week_ago).scalar()
    )
    new_entries_this_week = (
        db.query(func.count(Entry.id)).filter(Entry.created_at >= week_ago).scalar()
    )

    return PlatformStatsResponse(
        total_users=total_users or 0,
        active_users=active_users or 0,
        total_entries=total_entries or 0,
        total_analyses=total_analyses or 0,
        new_users_this_week=new_users_this_week or 0,
        new_entries_this_week=new_entries_this_week or 0,
    )


def list_all_users(
    db: Session,
    page: int = 1,
    limit: int = 10,
    search: Optional[str] = None,
) -> AdminUserListResponse:
    query = db.query(User)

    if search:
        term = f"%{search}%"
        query = query.filter(
            (User.email.ilike(term)) | (User.username.ilike(term))
        )

    total = query.count()
    users_db = query.order_by(User.created_at.desc()).offset((page - 1) * limit).limit(limit).all()

    # Lấy entry_count và last_entry_at cho từng user
    user_ids = [u.id for u in users_db]
    entry_stats = (
        db.query(
            Entry.user_id,
            func.count(Entry.id).label("entry_count"),
            func.max(Entry.created_at).label("last_entry_at"),
        )
        .filter(Entry.user_id.in_(user_ids))
        .group_by(Entry.user_id)
        .all()
    )
    stats_map = {row.user_id: row for row in entry_stats}

    items = []
    for u in users_db:
        stat = stats_map.get(u.id)
        items.append(
            AdminUserItem(
                id=u.id,
                email=u.email,
                username=u.username,
                display_name=u.display_name,
                is_active=u.is_active,
                role=u.role,
                created_at=u.created_at,
                entry_count=stat.entry_count if stat else 0,
                last_entry_at=stat.last_entry_at if stat else None,
            )
        )

    return AdminUserListResponse(users=items, total=total, page=page, limit=limit)


def toggle_user_active(
    db: Session, user_id: int, current_admin_id: int
) -> AdminToggleActiveResponse:
    if user_id == current_admin_id:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Không thể vô hiệu hóa chính mình")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")

    user.is_active = not user.is_active
    db.commit()
    db.refresh(user)

    action = "kích hoạt" if user.is_active else "vô hiệu hóa"
    return AdminToggleActiveResponse(
        id=user.id,
        is_active=user.is_active,
        message=f"Đã {action} tài khoản {user.username}",
    )
