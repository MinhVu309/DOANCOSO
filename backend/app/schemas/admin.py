from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class PlatformStatsResponse(BaseModel):
    total_users: int
    active_users: int
    total_entries: int
    total_analyses: int
    new_users_this_week: int
    new_entries_this_week: int


class AdminUserItem(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    email: str
    username: str
    display_name: Optional[str]
    is_active: bool
    role: str
    created_at: datetime
    entry_count: int
    last_entry_at: Optional[datetime]


class AdminUserListResponse(BaseModel):
    users: List[AdminUserItem]
    total: int
    page: int
    limit: int


class AdminToggleActiveResponse(BaseModel):
    id: int
    is_active: bool
    message: str
