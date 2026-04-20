from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..routers.auth import get_current_user
from ..schemas.trends import (
    MoodChartResponse, StreakResponse,
    MentalIndexResponse, TopEmotionsResponse,
)
from ..services import trends_service

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
