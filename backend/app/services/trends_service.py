from datetime import date, timedelta, datetime
from typing import Optional
from collections import Counter

from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models.entry import Entry
from ..models.analysis_result import AnalysisResult
from ..constants import EMOTION_MAPPING
from ..schemas.trends import (
    MoodChartResponse, MoodChartPoint,
    StreakResponse,
    MentalIndexResponse,
    TopEmotionsResponse, TopEmotionItem,
)


def _period_start(period: str) -> date:
    today = date.today()
    if period == "week":
        return today - timedelta(days=6)
    return today - timedelta(days=29)  # month = 30 days


def get_mood_chart(db: Session, user_id: int, period: str = "week") -> MoodChartResponse:
    start = _period_start(period)

    rows = (
        db.query(Entry.created_at, AnalysisResult.emotion_label, AnalysisResult.emotion_score)
        .join(AnalysisResult, AnalysisResult.entry_id == Entry.id)
        .filter(Entry.user_id == user_id, func.date(Entry.created_at) >= start)
        .order_by(Entry.created_at)
        .all()
    )

    data_points = []
    for created_at, emotion_label, _ in rows:
        mapping = EMOTION_MAPPING.get(emotion_label, EMOTION_MAPPING["Other"])
        data_points.append(MoodChartPoint(
            date=created_at.date() if hasattr(created_at, "date") else created_at,
            mood_score=mapping["mood_score"],
            emotion_label=emotion_label,
        ))

    return MoodChartResponse(period=period, data_points=data_points)


def get_streak(db: Session, user_id: int) -> StreakResponse:
    rows = (
        db.query(func.date(Entry.created_at).label("d"))
        .filter(Entry.user_id == user_id)
        .distinct()
        .order_by(func.date(Entry.created_at).desc())
        .all()
    )

    total = db.query(func.count(Entry.id)).filter(Entry.user_id == user_id).scalar() or 0
    dates = [r.d for r in rows]

    if not dates:
        return StreakResponse(current_streak=0, longest_streak=0, total_entries=0)

    # Normalize to date objects
    def to_date(d):
        if isinstance(d, str):
            return datetime.strptime(d, "%Y-%m-%d").date()
        if isinstance(d, datetime):
            return d.date()
        return d

    dates = sorted([to_date(d) for d in dates], reverse=True)
    today = date.today()

    # Current streak
    current = 0
    check = today
    for d in dates:
        if d == check:
            current += 1
            check -= timedelta(days=1)
        elif d == today - timedelta(days=1) and current == 0:
            # Allow yesterday to start streak
            current += 1
            check = d - timedelta(days=1)
        else:
            break

    # Longest streak
    longest = 1
    run = 1
    for i in range(1, len(dates)):
        if (dates[i - 1] - dates[i]).days == 1:
            run += 1
            longest = max(longest, run)
        else:
            run = 1

    return StreakResponse(
        current_streak=current,
        longest_streak=max(longest, current),
        total_entries=total,
        last_entry_date=dates[0],
    )


def _score_to_level(score: float) -> str:
    if score < 0.3:
        return "Thấp"
    if score < 0.6:
        return "Trung bình"
    return "Cao"


def get_mental_index(db: Session, user_id: int, period: str = "month") -> MentalIndexResponse:
    start = _period_start(period)

    def avg_score(*labels):
        rows = (
            db.query(func.avg(AnalysisResult.emotion_score))
            .join(Entry, Entry.id == AnalysisResult.entry_id)
            .filter(
                Entry.user_id == user_id,
                func.date(Entry.created_at) >= start,
                AnalysisResult.emotion_label.in_(labels),
            )
            .scalar()
        )
        return float(rows) if rows else 0.0

    stress_score = avg_score("Anger", "Fear")
    anxiety_score = avg_score("Fear")
    depression_score = avg_score("Sadness")

    return MentalIndexResponse(
        stress_level=_score_to_level(stress_score),
        stress_score=round(stress_score, 3),
        anxiety_level=_score_to_level(anxiety_score),
        anxiety_score=round(anxiety_score, 3),
        depression_level=_score_to_level(depression_score),
        depression_score=round(depression_score, 3),
        note="Các chỉ số này mang tính chất tham khảo, không thay thế đánh giá y tế chuyên nghiệp.",
    )


def get_top_emotions(db: Session, user_id: int, period: str = "week") -> TopEmotionsResponse:
    start = _period_start(period)

    rows = (
        db.query(AnalysisResult.emotion_label, func.count(AnalysisResult.id).label("cnt"))
        .join(Entry, Entry.id == AnalysisResult.entry_id)
        .filter(Entry.user_id == user_id, func.date(Entry.created_at) >= start)
        .group_by(AnalysisResult.emotion_label)
        .order_by(func.count(AnalysisResult.id).desc())
        .limit(6)
        .all()
    )

    emotions = []
    for label, count in rows:
        mapping = EMOTION_MAPPING.get(label, EMOTION_MAPPING["Other"])
        emotions.append(TopEmotionItem(
            label=label,
            label_vi=mapping["vi_casual"],
            count=count,
            color=mapping["color"],
        ))

    return TopEmotionsResponse(period=period, emotions=emotions)
