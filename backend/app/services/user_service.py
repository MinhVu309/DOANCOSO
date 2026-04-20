import os
import uuid
from datetime import time
from typing import Optional

from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session

from ..config import settings
from ..models.user_preference import UserPreference
from ..schemas.user import UserProfileUpdate, UserPreferencesUpdate


def get_or_create_preference(db: Session, user_id: int) -> UserPreference:
    pref = db.query(UserPreference).filter(UserPreference.user_id == user_id).first()
    if pref is None:
        pref = UserPreference(user_id=user_id)
        db.add(pref)
        db.commit()
        db.refresh(pref)
    return pref


def update_profile(db: Session, user_id: int, data: UserProfileUpdate) -> UserPreference:
    pref = get_or_create_preference(db, user_id)
    if data.display_name is not None:
        pref.display_name = data.display_name
    if data.birth_date is not None:
        pref.birth_date = data.birth_date
    if data.timezone is not None:
        pref.timezone = data.timezone
    db.commit()
    db.refresh(pref)
    return pref


async def update_avatar(db: Session, user_id: int, file: UploadFile) -> str:
    """Save uploaded avatar, return the URL path."""
    content = await file.read()
    if len(content) > settings.max_upload_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File quá lớn. Tối đa {settings.max_upload_size // (1024 * 1024)} MB.",
        )

    ext = (file.filename or "avatar").rsplit(".", 1)[-1].lower()
    if ext not in ("jpg", "jpeg", "png", "webp"):
        raise HTTPException(status_code=400, detail="Chỉ hỗ trợ JPG, PNG, WEBP.")

    avatars_dir = os.path.join(settings.upload_dir, "avatars")
    os.makedirs(avatars_dir, exist_ok=True)
    filename = f"{user_id}.{ext}"
    filepath = os.path.join(avatars_dir, filename)

    with open(filepath, "wb") as f:
        f.write(content)

    url_path = f"/uploads/avatars/{filename}"
    pref = get_or_create_preference(db, user_id)
    pref.avatar_url = url_path
    db.commit()
    return url_path


def delete_avatar(db: Session, user_id: int) -> None:
    pref = get_or_create_preference(db, user_id)
    if pref.avatar_url:
        filepath = pref.avatar_url.lstrip("/")
        if os.path.exists(filepath):
            os.remove(filepath)
        pref.avatar_url = None
        db.commit()


def get_preferences(db: Session, user_id: int) -> UserPreference:
    return get_or_create_preference(db, user_id)


def update_preferences(db: Session, user_id: int, data: UserPreferencesUpdate) -> UserPreference:
    pref = get_or_create_preference(db, user_id)
    if data.theme is not None:
        pref.theme = data.theme
    if data.reminder_enabled is not None:
        pref.reminder_enabled = data.reminder_enabled
    if data.reminder_time is not None:
        try:
            h, m = map(int, data.reminder_time.split(":"))
            pref.reminder_time = time(h, m)
        except (ValueError, AttributeError):
            raise HTTPException(status_code=400, detail="reminder_time phải có định dạng HH:MM")
    if data.reminder_days is not None:
        pref.reminder_days = data.reminder_days
    db.commit()
    db.refresh(pref)
    return pref
