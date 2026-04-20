import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..database import Base


class EntryTag(Base):
    __tablename__ = "entry_tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entry_id = Column(UUID(as_uuid=True), ForeignKey("entries.id", ondelete="CASCADE"), nullable=False, index=True)
    tag_name = Column(String(100), nullable=False)
    tag_type = Column(String(20), nullable=False, default="user_defined")  # "user_defined" | "ai_topic"

    entry = relationship("Entry", back_populates="tags")
