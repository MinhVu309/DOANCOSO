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

    # Tích lũy trong cửa sổ quan sát
    occurrence_count = Column(Integer, nullable=False, default=0)
    avg_confidence = Column(Float, nullable=False, default=0.0)

    first_seen_at = Column(DateTime(timezone=True), nullable=False)
    last_seen_at = Column(DateTime(timezone=True), nullable=False)

    # True khi warning_level in {'alert', 'urgent'}
    confirmed = Column(Boolean, nullable=False, default=False)

    # --- DSM-5/ICD-11 Early Warning fields ---
    # Per [1] APA DSM-5-TR (2022) and [2] WHO ICD-11 CDDR (2024)

    # 'watch' | 'alert' | 'urgent' | NULL — ICD-11 severity tiers [3] Reed et al. 2019
    warning_level = Column(String(10), nullable=True)

    # Weighted mean confidence (0.0–1.0) — proxy for symptom load [2] WHO ICD-11 CDDR
    intensity_score = Column(Float, nullable=True)

    # Most recent streak of consecutive days the condition appeared
    consecutive_days = Column(Integer, nullable=True)

    # Observation window (days) that triggered the current warning_level
    within_window_days = Column(Integer, nullable=True)

    # Timestamp when warning_level was last set or escalated — used for throttling
    last_warned_at = Column(DateTime(timezone=True), nullable=True)

    # Clinical coding per [1] DSM-5-TR and [2] ICD-11 CDDR
    dsm5_code = Column(String(20), nullable=True)
    icd11_code = Column(String(10), nullable=True)

    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
