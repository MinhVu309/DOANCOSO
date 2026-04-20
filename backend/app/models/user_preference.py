import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Date, Time, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.sql import func

from ..database import Base


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    display_name = Column(String(100), nullable=True)
    birth_date = Column(Date, nullable=True)
    timezone = Column(String(50), nullable=False, default="Asia/Ho_Chi_Minh")
    avatar_url = Column(String(255), nullable=True)
    theme = Column(String(20), nullable=False, default="light")
    reminder_enabled = Column(Boolean, nullable=False, default=False)
    reminder_time = Column(Time, nullable=True)
    reminder_days = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
