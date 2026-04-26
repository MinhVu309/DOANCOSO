import uuid
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from ..database import Base


class UserCondition(Base):
    __tablename__ = "user_conditions"
    __table_args__ = (
        UniqueConstraint("user_id", "condition_name", name="uq_user_condition"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    condition_name = Column(String(200), nullable=False)

    # Tích lũy trong cửa sổ 30 ngày gần nhất
    occurrence_count = Column(Integer, nullable=False, default=0)
    avg_confidence = Column(Float, nullable=False, default=0.0)

    first_seen_at = Column(DateTime(timezone=True), nullable=False)
    last_seen_at = Column(DateTime(timezone=True), nullable=False)

    # True khi occurrence_count >= MIN_OCCURRENCES
    confirmed = Column(Boolean, nullable=False, default=False)

    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
