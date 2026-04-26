from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..routers.auth import get_current_user
from ..schemas.trends import (
    MoodChartResponse, StreakResponse,
    MentalIndexResponse, TopEmotionsResponse,
    MentalHealthSummaryResponse,
)
from ..services import trends_service
from ..services.condition_service import get_user_conditions, CONDITION_WINDOW_DAYS, CONDITION_MIN_OCCURRENCES

router = APIRouter(prefix="/api/trends", tags=["Trends"])


@router.get("/mood-chart", response_model=MoodChartResponse)
def mood_chart(
    period: str = Query("week", pattern="^(week|month)$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return trends_service.get_mood_chart(db, current_user.id, period)


@router.get("/streak", response_model=StreakResponse)
def streak(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return trends_service.get_streak(db, current_user.id)


@router.get("/mental-index", response_model=MentalIndexResponse)
def mental_index(
    period: str = Query("month", pattern="^(week|month)$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return trends_service.get_mental_index(db, current_user.id, period)


@router.get("/top-emotions", response_model=TopEmotionsResponse)
def top_emotions(
    period: str = Query("week", pattern="^(week|month)$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return trends_service.get_top_emotions(db, current_user.id, period)


@router.get("/mental-health", response_model=MentalHealthSummaryResponse)
def mental_health_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Tra ve danh sach tinh trang tam than duoc tich luy tu nhieu bai viet.
    confirmed=True khi xuat hien >= 3 lan trong 30 ngay gan nhat.
    """
    conditions = get_user_conditions(db, current_user.id)
    return MentalHealthSummaryResponse(
        window_days=CONDITION_WINDOW_DAYS,
        min_occurrences=CONDITION_MIN_OCCURRENCES,
        conditions=conditions,
    )
