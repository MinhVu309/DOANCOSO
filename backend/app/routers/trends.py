from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..routers.auth import get_current_user
from ..schemas.trends import (
    MoodChartResponse, StreakResponse,
    MentalIndexResponse, TopEmotionsResponse,
    MentalHealthSummaryResponse, WarningDisclaimer,
)
from ..services import trends_service
from ..services.condition_service import (
    get_user_conditions,
    CONDITION_WINDOW_DAYS,
)

router = APIRouter(prefix="/api/trends", tags=["Trends"])

# Mandatory disclaimer per [1] APA DSM-5-TR (2022) and [2] WHO ICD-11 CDDR (2024).
# Must accompany every response that carries warning_level fields.
_WARNING_DISCLAIMER = WarningDisclaimer(
    vi=(
        "Kết quả này được tạo bởi AI dựa trên tín hiệu từ nhật ký của bạn. "
        "Đây KHÔNG phải chẩn đoán lâm sàng. Chẩn đoán chính thức yêu cầu "
        "đánh giá bởi chuyên gia tâm lý hoặc bác sĩ tâm thần có chuyên môn."
    ),
    source=(
        "Per [1] APA DSM-5-TR (2022) and [2] WHO ICD-11 CDDR (2024): "
        "diagnosis requires clinician evaluation, not AI screening alone."
    ),
)


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
    Returns accumulated mental-health conditions with DSM-5/ICD-11 warning levels.

    warning_level semantics (per [3] Reed et al. 2019 ICD-11 utility framework):
      'watch'  — subthreshold, frequency/duration not yet at clinical threshold
      'alert'  — approaching threshold, self-care resources recommended
      'urgent' — meets / exceeds DSM-5 [1] or ICD-11 [2] threshold,
                 professional evaluation strongly recommended

    Response always includes a disclaimer confirming this is AI screening,
    not a clinical diagnosis [1][2].
    """
    conditions = get_user_conditions(db, current_user.id)
    return MentalHealthSummaryResponse(
        window_days=CONDITION_WINDOW_DAYS,
        conditions=conditions,
        disclaimer=_WARNING_DISCLAIMER,
    )
