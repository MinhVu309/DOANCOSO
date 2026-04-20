from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


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
    analyzed_at: datetime
