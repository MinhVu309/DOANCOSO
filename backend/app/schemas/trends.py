from typing import List, Optional
from datetime import date
from pydantic import BaseModel


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
