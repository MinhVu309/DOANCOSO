from fastapi import APIRouter, Depends, UploadFile, File, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..routers.auth import get_current_user
from ..schemas.user import (
    UserProfileUpdate, UserProfileResponse,
    UserPreferencesUpdate, UserPreferencesResponse,
)
from ..services import user_service

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("/me/profile", response_model=UserProfileResponse)
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    pref = user_service.get_or_create_preference(db, current_user.id)
    return UserProfileResponse(
        display_name=pref.display_name or current_user.display_name,
        email=current_user.email,
        birth_date=pref.birth_date,
        timezone=pref.timezone,
        avatar_url=pref.avatar_url,
    )


@router.put("/me/profile", response_model=UserProfileResponse)
def update_profile(
    data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    pref = user_service.update_profile(db, current_user.id, data)
    return UserProfileResponse(
        display_name=pref.display_name or current_user.display_name,
        email=current_user.email,
        birth_date=pref.birth_date,
        timezone=pref.timezone,
        avatar_url=pref.avatar_url,
    )


@router.post("/me/avatar", status_code=status.HTTP_200_OK)
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    url = await user_service.update_avatar(db, current_user.id, file)
    return {"avatar_url": url}


@router.delete("/me/avatar", status_code=status.HTTP_204_NO_CONTENT)
def delete_avatar(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_service.delete_avatar(db, current_user.id)


@router.get("/me/preferences", response_model=UserPreferencesResponse)
def get_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    pref = user_service.get_preferences(db, current_user.id)
    return UserPreferencesResponse(
        theme=pref.theme,
        reminder_enabled=pref.reminder_enabled,
        reminder_time=pref.reminder_time.strftime("%H:%M") if pref.reminder_time else None,
        reminder_days=pref.reminder_days or [],
    )


@router.put("/me/preferences", response_model=UserPreferencesResponse)
def update_preferences(
    data: UserPreferencesUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    pref = user_service.update_preferences(db, current_user.id, data)
    return UserPreferencesResponse(
        theme=pref.theme,
        reminder_enabled=pref.reminder_enabled,
        reminder_time=pref.reminder_time.strftime("%H:%M") if pref.reminder_time else None,
        reminder_days=pref.reminder_days or [],
    )
