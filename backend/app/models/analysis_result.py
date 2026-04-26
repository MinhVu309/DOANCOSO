import uuid
from sqlalchemy import Column, String, Float, Boolean, DateTime, Text, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..database import Base


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entry_id = Column(UUID(as_uuid=True), ForeignKey("entries.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)

    # Kết quả Module-1
    emotion_label = Column(String(50), nullable=False)
    emotion_score = Column(Float, nullable=False)
    hate_label = Column(String(50), nullable=False)
    hate_score = Column(Float, nullable=False)
    needs_assessment = Column(Boolean, nullable=False, default=False)

    # Kết quả Module-2 (nullable khi chưa có)
    condition = Column(String(100), nullable=True)
    condition_confidence = Column(Float, nullable=True)
    severity = Column(String(50), nullable=True)
    conditions = Column(JSON, nullable=True)  # top-5: [{"label": str, "confidence": float}]

    # Derived fields
    mood_label_vi = Column(String(50), nullable=False)
    mood_color = Column(String(20), nullable=False)
    ai_summary = Column(Text, nullable=False)
    ai_tags = Column(JSON, nullable=False, default=list)

    # Meta
    analyzed_at = Column(DateTime(timezone=True), server_default=func.now())
    raw_response = Column(JSON, nullable=True)

    entry = relationship("Entry", back_populates="analysis_result")
