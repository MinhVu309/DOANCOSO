from collections import defaultdict
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from ..models.analysis_result import AnalysisResult
from ..models.user_condition import UserCondition

CONDITION_WINDOW_DAYS = 30
CONDITION_MIN_OCCURRENCES = 3
CONDITION_MIN_CONFIDENCE = 0.3


def aggregate_user_conditions(db: Session, user_id: int) -> None:
    """
    Quét toan bo analysis_results cua user trong 30 ngay gan nhat,
    dem so lan xuat hien moi condition, upsert vao user_conditions.
    Goi sau moi analyze_entry thanh cong.
    """
    from ..models.entry import Entry

    cutoff = datetime.now(timezone.utc) - timedelta(days=CONDITION_WINDOW_DAYS)

    rows = (
        db.query(AnalysisResult, Entry.created_at)
        .join(Entry, Entry.id == AnalysisResult.entry_id)
        .filter(Entry.user_id == user_id)
        .filter(Entry.created_at >= cutoff)
        .filter(AnalysisResult.conditions.isnot(None))
        .all()
    )

    counts: dict[str, int] = defaultdict(int)
    sum_conf: dict[str, float] = defaultdict(float)
    first_seen: dict[str, datetime] = {}
    last_seen: dict[str, datetime] = {}

    for result, entry_date in rows:
        for cond in (result.conditions or []):
            conf = cond.get("confidence", 0.0)
            if conf < CONDITION_MIN_CONFIDENCE:
                continue
            name = cond["label"]
            counts[name] += 1
            sum_conf[name] += conf
            if name not in first_seen or entry_date < first_seen[name]:
                first_seen[name] = entry_date
            if name not in last_seen or entry_date > last_seen[name]:
                last_seen[name] = entry_date

    for name, count in counts.items():
        avg_conf = round(sum_conf[name] / count, 4)
        confirmed = count >= CONDITION_MIN_OCCURRENCES

        existing = (
            db.query(UserCondition)
            .filter(UserCondition.user_id == user_id, UserCondition.condition_name == name)
            .first()
        )

        if existing:
            existing.occurrence_count = count
            existing.avg_confidence = avg_conf
            existing.last_seen_at = last_seen[name]
            existing.confirmed = confirmed
        else:
            db.add(UserCondition(
                user_id=user_id,
                condition_name=name,
                occurrence_count=count,
                avg_confidence=avg_conf,
                first_seen_at=first_seen[name],
                last_seen_at=last_seen[name],
                confirmed=confirmed,
            ))

    db.commit()


def get_user_conditions(db: Session, user_id: int) -> list[UserCondition]:
    """Tra ve tat ca conditions cua user, confirmed truoc, sort theo so lan xuat hien."""
    return (
        db.query(UserCondition)
        .filter(UserCondition.user_id == user_id)
        .order_by(UserCondition.confirmed.desc(), UserCondition.occurrence_count.desc())
        .all()
    )
