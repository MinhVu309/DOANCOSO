from uuid import UUID

import httpx
from sqlalchemy.orm import Session

from ..config import settings
from ..constants import EMOTION_MAPPING, AI_SUMMARY_TEMPLATES, AI_TAGS_BY_EMOTION
from ..models.analysis_result import AnalysisResult
from .condition_service import aggregate_user_conditions

HATE_MIN_CONFIDENCE = 0.5

# Map nhan 28-label sang nhom cu de generate summary/tags van dung duoc
_EMOTION_TO_SUMMARY_GROUP: dict[str, str] = {
    'amusement': 'Enjoyment', 'excitement': 'Enjoyment', 'joy': 'Enjoyment',
    'love': 'Enjoyment', 'desire': 'Enjoyment', 'optimism': 'Enjoyment',
    'caring': 'Enjoyment', 'pride': 'Enjoyment', 'admiration': 'Enjoyment',
    'gratitude': 'Enjoyment', 'relief': 'Enjoyment', 'approval': 'Enjoyment',
    'realization': 'Surprise', 'surprise': 'Surprise', 'curiosity': 'Surprise',
    'confusion': 'Other',
    'fear': 'Fear', 'nervousness': 'Fear',
    'remorse': 'Sadness', 'embarrassment': 'Sadness', 'disappointment': 'Sadness',
    'sadness': 'Sadness', 'grief': 'Sadness',
    'disgust': 'Disgust', 'disapproval': 'Disgust',
    'anger': 'Anger', 'annoyance': 'Anger',
    'neutral': 'Other',
}


async def analyze_entry(db: Session, entry_id: UUID) -> AnalysisResult:
    """Call Module-1, parse result, upsert AnalysisResult row, return it."""
    from ..models.entry import Entry  # avoid circular import

    entry = db.query(Entry).filter(Entry.id == entry_id).first()
    if entry is None:
        raise ValueError(f"Entry {entry_id} not found")

    raw: dict = {}
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                f"{settings.module1_url}/api/analyze",
                json={"text": entry.content},
            )
            resp.raise_for_status()
            raw = resp.json()
    except Exception:
        # Module-1 unavailable — store empty result so entry is still saved
        return _upsert_empty_analysis(db, entry_id)

    # Module-1 ver 2.6: multi-label emotions (list), hate / hate_score
    emotions: list = raw.get("emotions", [])
    emotion_label: str = emotions[0] if emotions else "neutral"

    # Lay score cua primary emotion tu emotion_scores list
    emotion_scores_list: list = raw.get("emotion_scores", [])
    emotion_score: float = next(
        (s["confidence"] for s in emotion_scores_list if s["label"] == emotion_label),
        0.0,
    )

    hate_label: str = raw.get("hate", raw.get("hate_speech", "Clean"))
    hate_score: float = raw.get("hate_score", raw.get("hate_confidence", 0.0))

    if hate_score < HATE_MIN_CONFIDENCE:
        hate_label = "Clean"

    needs_assessment: bool = raw.get("needs_assessment", False)

    assessment = raw.get("assessment") or {}
    condition = assessment.get("condition")
    condition_confidence = assessment.get("confidence")
    severity = assessment.get("severity")
    conditions = assessment.get("conditions")  # top-5 list từ Module-2

    summary_group = _EMOTION_TO_SUMMARY_GROUP.get(emotion_label, "Other")
    mapping = EMOTION_MAPPING.get(summary_group, EMOTION_MAPPING["Other"])
    mood_label_vi = mapping["vi"]
    mood_color = mapping["color"]
    ai_summary = generate_ai_summary(summary_group, hate_label)
    ai_tags = AI_TAGS_BY_EMOTION.get(summary_group, [])

    # Upsert: delete existing if any, then insert
    existing = db.query(AnalysisResult).filter(AnalysisResult.entry_id == entry_id).first()
    if existing:
        db.delete(existing)
        db.flush()

    result = AnalysisResult(
        entry_id=entry_id,
        emotion_label=emotion_label,
        emotion_score=emotion_score,
        hate_label=hate_label,
        hate_score=hate_score,
        needs_assessment=needs_assessment,
        condition=condition,
        condition_confidence=condition_confidence,
        severity=severity,
        conditions=conditions,
        mood_label_vi=mood_label_vi,
        mood_color=mood_color,
        ai_summary=ai_summary,
        ai_tags=ai_tags,
        raw_response=raw,
    )
    db.add(result)
    db.commit()
    db.refresh(result)

    # Tich luy du lieu condition sau moi bai analyze
    aggregate_user_conditions(db, entry.user_id)

    return result


def generate_ai_summary(emotion_label: str, hate_label: str) -> str:
    key = (emotion_label, hate_label)
    return AI_SUMMARY_TEMPLATES.get(key, "Một ngày với nhiều cảm xúc khác nhau.")


def _upsert_empty_analysis(db: Session, entry_id: UUID) -> AnalysisResult:
    existing = db.query(AnalysisResult).filter(AnalysisResult.entry_id == entry_id).first()
    if existing:
        return existing

    mapping = EMOTION_MAPPING["Other"]
    result = AnalysisResult(
        entry_id=entry_id,
        emotion_label="neutral",
        emotion_score=0.0,
        hate_label="Clean",
        hate_score=0.0,
        needs_assessment=False,
        mood_label_vi=mapping["vi"],
        mood_color=mapping["color"],
        ai_summary="Module AI chưa sẵn sàng, kết quả sẽ được cập nhật sau.",
        ai_tags=[],
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


async def check_module1_health() -> bool:
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"{settings.module1_url}/health")
            return resp.status_code == 200
    except Exception:
        return False
