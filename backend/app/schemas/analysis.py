from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator


class ConditionScore(BaseModel):
    label: str
    confidence: float


class AnalysisResultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    emotion_label: str
    emotion_score: float
    hate_label: str
    needs_assessment: bool
    mood_label_vi: str
    mood_color: str
    ai_summary: str
    ai_tags: List[str]
    condition: Optional[str] = None
    condition_confidence: Optional[float] = None
    conditions: Optional[List[ConditionScore]] = None
    analyzed_at: datetime
    # raw_response dung de lay danh sach day du cac cam xuc (emotions list)
    raw_response: Optional[Dict[str, Any]] = None

    @field_validator("raw_response", mode="before")
    @classmethod
    def _drop_heavy_fields(cls, v):
        """Chi giu lai truong emotions tu raw_response de giam payload."""
        if not isinstance(v, dict):
            return None
        return {"emotions": v.get("emotions", [])} if v.get("emotions") else None
