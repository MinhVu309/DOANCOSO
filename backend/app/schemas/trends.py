from typing import List, Optional
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict


class MoodChartPoint(BaseModel):
    date: date
    mood_score: float
    emotion_label: str


class MoodChartResponse(BaseModel):
    period: str
    data_points: List[MoodChartPoint]


class StreakResponse(BaseModel):
    current_streak: int
    longest_streak: int
    total_entries: int
    last_entry_date: Optional[date] = None


class MentalIndexResponse(BaseModel):
    stress_level: str
    stress_score: float
    anxiety_level: str
    anxiety_score: float
    depression_level: str
    depression_score: float
    note: str


class TopEmotionItem(BaseModel):
    label: str
    label_vi: str
    count: int
    color: str


class TopEmotionsResponse(BaseModel):
    period: str
    emotions: List[TopEmotionItem]


class UserConditionItem(BaseModel):
    """
    Single condition row with DSM-5/ICD-11 early-warning fields.

    warning_level tiers per [3] Reed et al. (2019) ICD-11 utility framework:
      'watch'  → subthreshold, monitor only
      'alert'  → approaching threshold, self-care suggested
      'urgent' → meets/exceeds threshold, professional help recommended

    LIMITATION: AI-assisted screening proxy — not a clinical diagnosis.
    Per [1] APA DSM-5-TR (2022) and [2] WHO ICD-11 CDDR (2024).
    """
    model_config = ConfigDict(from_attributes=True)

    condition_name: str
    occurrence_count: int
    avg_confidence: float
    first_seen_at: datetime
    last_seen_at: datetime
    confirmed: bool

    # DSM-5/ICD-11 early-warning fields
    warning_level: Optional[str] = None       # 'watch' | 'alert' | 'urgent'
    intensity_score: Optional[float] = None   # weighted mean confidence (0–1)
    consecutive_days: Optional[int] = None    # most recent streak
    within_window_days: Optional[int] = None  # observation window used
    last_warned_at: Optional[datetime] = None
    dsm5_code: Optional[str] = None
    icd11_code: Optional[str] = None


class WarningDisclaimer(BaseModel):
    """
    Mandatory disclaimer per [1] APA DSM-5-TR (2022) and [2] WHO ICD-11 CDDR (2024).
    Must accompany every API response containing warning_level fields.
    """
    vi: str
    source: str


class MentalHealthSummaryResponse(BaseModel):
    window_days: int
    conditions: List[UserConditionItem]
    disclaimer: WarningDisclaimer
