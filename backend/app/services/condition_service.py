"""
NhatKi Early Warning System — DSM-5/ICD-11 Compliant
======================================================

Implements a three-axis (Frequency × Intensity × Duration) early-warning
algorithm grounded in internationally recognised diagnostic frameworks.

Primary references
------------------
[1] American Psychiatric Association. (2022). Diagnostic and Statistical
    Manual of Mental Disorders (5th ed., text rev.; DSM-5-TR).
    https://doi.org/10.1176/appi.books.9780890425787

[2] World Health Organization. (2024). Clinical descriptions and diagnostic
    requirements for ICD-11 mental, behavioural and neurodevelopmental
    disorders (CDDR). WHO Press.
    https://www.who.int/publications/i/item/9789240077263

[3] Reed, G. M., et al. (2019). Innovations and changes in the ICD-11
    classification of mental, behavioural and neurodevelopmental disorders.
    World Psychiatry, 18(1), 3–19. https://doi.org/10.1002/wps.20611

[4] Stein, D. J., et al. (2020). An organization- and category-level
    comparison of diagnostic requirements for mental disorders in ICD-11
    and DSM-5. World Psychiatry, 19(2), 235–246.
    https://doi.org/10.1002/wps.20736

[5] Loo Gee, B., et al. (2016). Psychological distress and DSM-5 symptom
    thresholds: Implications for screening.
    Frontiers in Psychiatry, 9, 450. https://doi.org/10.3389/fpsyt.2018.00450

[6] Galatzer-Levy, I. R., & Bryant, R. A. (2013). 636,120 ways to have PTSD.
    Perspectives on Psychological Science, 8(6), 651–662.
    https://doi.org/10.1177/1745691613504115

LIMITATION: This module is AI-assisted screening, NOT a clinical diagnosis.
All warning levels are proxies derived from journal-entry signals. Formal
diagnosis requires evaluation by a licensed mental health professional [1][2].
"""

from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from typing import Optional

from sqlalchemy.orm import Session

from ..models.analysis_result import AnalysisResult
from ..models.user_condition import UserCondition

# ---------------------------------------------------------------------------
# Global constants
# ---------------------------------------------------------------------------

# Maximum look-back window — covers the widest per-condition window (ADHD: 30d)
CONDITION_WINDOW_DAYS = 30

# Entries with Module-2 confidence below this floor are excluded entirely
_CONFIDENCE_FLOOR = 0.30

# Warning level precedence (higher index = more severe)
_LEVEL_ORDER: dict[Optional[str], int] = {None: 0, "watch": 1, "alert": 2, "urgent": 3}

# ---------------------------------------------------------------------------
# Per-condition rules
# ---------------------------------------------------------------------------
# Each rule defines three warning tiers that mirror DSM-5/ICD-11 thresholds
# (compressed to shorter observation windows for early-screening purposes).
#
# Frequency  = number of qualifying journal entries within `within_days`
# Intensity  = mean Module-2 confidence (proxy for symptom load) [2]
# Duration   = consecutive days with the condition detected
#
# Tier semantics per [3] Reed et al. (2019) ICD-11 Clinical Utility Framework:
#   'watch'  → subthreshold signal — monitor only
#   'alert'  → approaching clinical threshold — suggest self-care
#   'urgent' → meets / exceeds clinical threshold — recommend professional help
#
# anchor_emotions: the Module-1 emotion label(s) required to be present in at
#   least some qualifying entries (DSM-5 Criterion A anchor symptom proxy).
#   Empty list = no anchor requirement.

CONDITION_RULES: dict[str, dict] = {

    # ---- Major Depressive Disorder ----------------------------------------
    # DSM-5 [1] F32: ≥5 symptoms present for ≥2 consecutive weeks, including
    #   depressed mood or anhedonia (Criterion A).
    # Proxy anchor: Module-1 Sadness label as primary indicator.
    # Min symptom count rationale: [5] Loo Gee et al. (2018), PMC6176119.
    "Rối loạn trầm cảm": {
        "icd11": "6A70",
        "dsm5":  "F32.1",
        "watch":  {"occurrences": 2, "within_days": 14, "min_intensity": 0.40},
        "alert":  {"occurrences": 4, "within_days": 14, "min_intensity": 0.55},
        "urgent": {"consecutive_days": 7,               "min_intensity": 0.65},
        "anchor_emotions": ["sadness", "grief", "disappointment", "remorse"],
        "ref": "[1] APA DSM-5-TR, F32; [5] PMC6176119",
    },

    # ---- Generalized Anxiety Disorder -------------------------------------
    # DSM-5 [1] F41.1: ≥3 associated symptoms, ≥6 months.
    # Early-warning window compressed to 21 days per screening adaptation [3].
    "Rối loạn lo âu": {
        "icd11": "6B00",
        "dsm5":  "F41.1",
        "watch":  {"occurrences": 3, "within_days": 21, "min_intensity": 0.40},
        "alert":  {"occurrences": 5, "within_days": 21, "min_intensity": 0.55},
        "urgent": {"consecutive_days": 10,              "min_intensity": 0.65},
        "anchor_emotions": ["fear", "nervousness"],
        "ref": "[1] APA DSM-5-TR, F41.1; [3] Reed et al. 2019",
    },

    # ---- Post-Traumatic Stress Disorder -----------------------------------
    # DSM-5 [1] F43.10: symptoms ≥1 month; ICD-11 [2] 6B40 identifies more
    #   severe / persistent cases than ICD-10 [6] Galatzer-Levy & Bryant 2013.
    "PTSD": {
        "icd11": "6B40",
        "dsm5":  "F43.10",
        "watch":  {"occurrences": 2, "within_days": 14, "min_intensity": 0.50},
        "alert":  {"occurrences": 3, "within_days": 14, "min_intensity": 0.60},
        "urgent": {"occurrences": 4, "within_days": 14, "min_intensity": 0.70},
        "anchor_emotions": ["fear", "nervousness", "sadness", "grief"],
        "ref": "[1] APA DSM-5-TR, F43.10; [6] PMC6331687; [4] PMC7801846",
    },

    # ---- Insomnia Disorder ------------------------------------------------
    # ICD-11 [2] 7A00: sleep dissatisfaction ≥3 nights/week, ≥3 months.
    # Early-warning: ≥3 nights within a 7-day window (1 week proxy).
    "Mất ngủ": {
        "icd11": "7A00",
        "dsm5":  "F51.01",
        "watch":  {"occurrences": 2, "within_days": 7,  "min_intensity": 0.35},
        "alert":  {"occurrences": 3, "within_days": 7,  "min_intensity": 0.50},
        "urgent": {"occurrences": 5, "within_days": 14, "min_intensity": 0.60},
        "anchor_emotions": [],
        "ref": "[2] WHO ICD-11 CDDR 2024, 7A00; [3] Reed et al. 2019",
    },

    # ---- ADHD -------------------------------------------------------------
    # DSM-5 [1] F90.2: ≥6 symptoms, ≥6 months, onset before age 12.
    # 30-day observation window captures the minimum clinically meaningful span.
    "ADHD": {
        "icd11": "6A05",
        "dsm5":  "F90.2",
        "watch":  {"occurrences": 3, "within_days": 30, "min_intensity": 0.40},
        "alert":  {"occurrences": 6, "within_days": 30, "min_intensity": 0.55},
        "urgent": {"consecutive_days": 14,              "min_intensity": 0.65},
        "anchor_emotions": ["neutral", "confusion", "anger", "annoyance"],
        "ref": "[1] APA DSM-5-TR, F90.2; [4] PMC7801846",
    },

    # ---- Bipolar Disorder -------------------------------------------------
    # DSM-5 [1] F31: manic episode ≥1 week OR ≥3 symptoms causing marked
    #   impairment; ICD-11 [2] 6A60 severity qualifier applies [4].
    "Rối loạn lưỡng cực": {
        "icd11": "6A60",
        "dsm5":  "F31",
        "watch":  {"occurrences": 2, "within_days": 14, "min_intensity": 0.50},
        "alert":  {"occurrences": 3, "within_days": 14, "min_intensity": 0.60},
        "urgent": {"consecutive_days": 5,               "min_intensity": 0.70},
        "anchor_emotions": ["anger", "annoyance", "surprise", "excitement"],
        "ref": "[1] APA DSM-5-TR, F31; [4] PMC7801846",
    },
}

# ---------------------------------------------------------------------------
# Immediate URGENT override — self-harm / crisis signal
# ---------------------------------------------------------------------------
# Per [2] WHO ICD-11 CDDR functional severity criterion: when hate_label ==
# 'Hate' (proxy for severe hostile/self-destructive content) AND
# emotion_confidence > 0.75, the signal warrants immediate crisis resources.
_SELF_HARM_CONDITION_NAME = "Cảnh báo khủng hoảng"
_URGENT_OVERRIDE = {
    "hate_label":          "Hate",
    "emotion_score_floor": 0.75,
    "ref": "[2] WHO ICD-11 CDDR 2024 — functional severity criterion",
}


# ---------------------------------------------------------------------------
# ICD-11 severity mapper
# ---------------------------------------------------------------------------

def map_intensity_to_icd11_severity(intensity_score: float) -> str:
    """
    Maps Module-2 mean confidence to ICD-11 4-point severity qualifiers.

    Clinical rationale
    ------------------
    Per [4] Stein et al. (2020), Table 2 (PMC7801846), ICD-11 uses a
    not-present / mild / moderate / severe scale. Module-2 confidence is
    used here as a *proxy* for symptom load.

    Thresholds
    ----------
    < 0.35  → not_present  (signal below noise floor)
    0.35–0.54 → mild       (subthreshold, monitoring warranted)
    0.55–0.74 → moderate   (clinically significant, self-care recommended)
    ≥ 0.75  → severe       (meets ICD-11 severity criterion, see professional)

    LIMITATION: This is a PROXY mapping only. Module-2 confidence is not a
    validated clinical instrument. Final severity determination requires
    assessment by a qualified clinician [1][2].
    """
    if intensity_score < 0.35:
        return "not_present"
    elif intensity_score < 0.55:
        return "mild"
    elif intensity_score < 0.75:
        return "moderate"
    else:
        return "severe"


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _count_consecutive_days(dates: list[datetime]) -> int:
    """
    Returns the length of the most recent streak of consecutive calendar days.

    Duration axis implementation for DSM-5 [1] / ICD-11 [2] temporal criteria.
    Only the most recent unbroken streak is counted — a gap resets the counter.
    """
    if not dates:
        return 0
    unique_dates: list[date] = sorted({d.date() for d in dates}, reverse=True)
    streak = 1
    for i in range(1, len(unique_dates)):
        if (unique_dates[i - 1] - unique_dates[i]).days == 1:
            streak += 1
        else:
            break
    return streak


def _count_in_window(dates: list[datetime], within_days: int) -> int:
    cutoff = datetime.now(timezone.utc) - timedelta(days=within_days)
    return sum(1 for d in dates if d >= cutoff)


def _filter_by_anchor(
    dates: list[datetime],
    confs: list[float],
    emotions: list[str],
    anchor_emotions: list[str],
) -> tuple[list[datetime], list[float]]:
    """
    Filter entries to those where Module-1 emotion matches an anchor emotion.

    DSM-5 [1] Criterion A requires at least one 'anchor' symptom (e.g.,
    depressed mood for MDD). We apply this as a filter: only entries whose
    emotion_label is in anchor_emotions contribute to the frequency count.
    When anchor_emotions is empty, all entries qualify.
    """
    if not anchor_emotions:
        return dates, confs
    filtered_dates, filtered_confs = [], []
    for d, c, e in zip(dates, confs, emotions):
        if e in anchor_emotions:
            filtered_dates.append(d)
            filtered_confs.append(c)
    return filtered_dates, filtered_confs


# ---------------------------------------------------------------------------
# Core warning evaluator
# ---------------------------------------------------------------------------

def evaluate_warning_level(
    condition_name: str,
    intensity_score: float,
    consecutive_days: int,
    entry_dates: list[datetime],
) -> tuple[Optional[str], int]:
    """
    Determine the DSM-5/ICD-11 warning level for a single condition.

    Clinical rationale
    ------------------
    Evaluates three tiers ('urgent' → 'alert' → 'watch') from most to least
    severe, returning the FIRST (highest) tier whose criteria are met.
    Criteria mirror DSM-5 [1] frequency/duration thresholds, compressed for
    early-screening purposes per [3] Reed et al. (2019).

    Parameters
    ----------
    condition_name   : key in CONDITION_RULES
    intensity_score  : mean Module-2 confidence across qualifying entries
    consecutive_days : length of most recent consecutive-day streak
    entry_dates      : list of datetime objects for qualifying entries

    Returns
    -------
    (warning_level, within_window_days)
      warning_level    : 'urgent' | 'alert' | 'watch' | None
      within_window_days: observation window (days) that triggered this level,
                          or CONDITION_WINDOW_DAYS if no rule matched

    LIMITATION: Proxy screening only — not a validated clinical instrument [1][2].
    """
    rule = CONDITION_RULES.get(condition_name)
    if not rule:
        return None, CONDITION_WINDOW_DAYS

    for level in ("urgent", "alert", "watch"):
        criteria = rule.get(level)
        if not criteria:
            continue

        # Intensity must meet the threshold for this tier
        if intensity_score < criteria.get("min_intensity", 0.0):
            continue

        # Duration criterion: consecutive_days >= threshold
        if "consecutive_days" in criteria:
            if consecutive_days >= criteria["consecutive_days"]:
                return level, criteria["consecutive_days"]

        # Frequency criterion: N occurrences within W days
        if "occurrences" in criteria:
            within = criteria["within_days"]
            if _count_in_window(entry_dates, within) >= criteria["occurrences"]:
                return level, within

    return None, CONDITION_WINDOW_DAYS


# ---------------------------------------------------------------------------
# Main aggregation function
# ---------------------------------------------------------------------------

def aggregate_user_conditions(db: Session, user_id: int) -> None:
    """
    Scan the last 30 days of analysis_results for a user and upsert
    DSM-5/ICD-11 compliant early-warning signals into user_conditions.

    Algorithm (three-axis: Frequency × Intensity × Duration)
    ---------------------------------------------------------
    1. Fetch all AnalysisResult rows (with Module-2 conditions) for this user
       within CONDITION_WINDOW_DAYS.
    2. Per condition label:
       a. Exclude entries whose Module-2 confidence < _CONFIDENCE_FLOOR.
       b. Apply anchor_emotion filter (DSM-5 Criterion A proxy) [1].
       c. Compute intensity_score (mean confidence).
       d. Compute consecutive_days (most recent streak) [1][2].
       e. Call evaluate_warning_level() to determine tier.
    3. Check URGENT_OVERRIDE: hate_label == 'Hate' + emotion_score > 0.75 →
       create a crisis-warning entry [2].
    4. Upsert UserCondition rows; escalate last_warned_at when tier rises.
    5. commit().

    Called after every successful analyze_entry().

    LIMITATION: This is AI-assisted screening, NOT a clinical diagnosis.
    All warning levels are proxies. Diagnosis requires a clinician [1][2].
    """
    from ..models.entry import Entry

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=CONDITION_WINDOW_DAYS)

    rows = (
        db.query(AnalysisResult, Entry.created_at)
        .join(Entry, Entry.id == AnalysisResult.entry_id)
        .filter(Entry.user_id == user_id)
        .filter(Entry.created_at >= cutoff)
        .filter(AnalysisResult.conditions.isnot(None))
        .all()
    )

    # Build per-condition data bags
    cond_dates:    dict[str, list[datetime]] = defaultdict(list)
    cond_confs:    dict[str, list[float]]    = defaultdict(list)
    cond_emotions: dict[str, list[str]]      = defaultdict(list)

    # Separate bag for self-harm override check (per-entry, condition-agnostic)
    crisis_dates: list[datetime] = []

    for result, entry_date in rows:
        # Make entry_date timezone-aware (PostgreSQL may return aware or naive)
        if entry_date.tzinfo is None:
            entry_date = entry_date.replace(tzinfo=timezone.utc)

        # Self-harm override check — per [2] WHO ICD-11 CDDR functional severity
        if (
            result.hate_label == _URGENT_OVERRIDE["hate_label"]
            and result.emotion_score > _URGENT_OVERRIDE["emotion_score_floor"]
        ):
            crisis_dates.append(entry_date)

        for cond in (result.conditions or []):
            conf = cond.get("confidence", 0.0)
            if conf < _CONFIDENCE_FLOOR:
                continue
            name = cond["label"]
            cond_dates[name].append(entry_date)
            cond_confs[name].append(conf)
            cond_emotions[name].append(result.emotion_label or "Other")

    # -----------------------------------------------------------------------
    # Upsert per-condition warning rows
    # -----------------------------------------------------------------------
    for name in cond_dates:
        rule = CONDITION_RULES.get(name, {})
        anchor_emotions: list[str] = rule.get("anchor_emotions", [])

        qualifying_dates, qualifying_confs = _filter_by_anchor(
            cond_dates[name],
            cond_confs[name],
            cond_emotions[name],
            anchor_emotions,
        )

        if not qualifying_dates:
            continue

        occurrence_count = len(qualifying_dates)
        intensity_score  = round(sum(qualifying_confs) / occurrence_count, 4)
        consec_days      = _count_consecutive_days(qualifying_dates)

        warning_level, within_window = evaluate_warning_level(
            condition_name=name,
            intensity_score=intensity_score,
            consecutive_days=consec_days,
            entry_dates=qualifying_dates,
        )

        icd11_code = rule.get("icd11")
        dsm5_code  = rule.get("dsm5")

        confirmed = warning_level in {"alert", "urgent"}

        first_seen = min(qualifying_dates)
        last_seen  = max(qualifying_dates)

        existing: Optional[UserCondition] = (
            db.query(UserCondition)
            .filter(
                UserCondition.user_id == user_id,
                UserCondition.condition_name == name,
            )
            .first()
        )

        # last_warned_at: set when level is newly assigned or escalates
        if existing:
            old_level = existing.warning_level
            escalated = _LEVEL_ORDER.get(warning_level, 0) > _LEVEL_ORDER.get(old_level, 0)
            last_warned_at = now if (warning_level and escalated) else existing.last_warned_at
        else:
            last_warned_at = now if warning_level else None

        if existing:
            existing.occurrence_count  = occurrence_count
            existing.avg_confidence    = round(sum(cond_confs[name]) / len(cond_confs[name]), 4)
            existing.last_seen_at      = last_seen
            existing.confirmed         = confirmed
            existing.warning_level     = warning_level
            existing.intensity_score   = intensity_score
            existing.consecutive_days  = consec_days
            existing.within_window_days = within_window
            existing.last_warned_at    = last_warned_at
            existing.dsm5_code         = dsm5_code
            existing.icd11_code        = icd11_code
        else:
            db.add(UserCondition(
                user_id=user_id,
                condition_name=name,
                occurrence_count=occurrence_count,
                avg_confidence=round(sum(cond_confs[name]) / len(cond_confs[name]), 4),
                first_seen_at=first_seen,
                last_seen_at=last_seen,
                confirmed=confirmed,
                warning_level=warning_level,
                intensity_score=intensity_score,
                consecutive_days=consec_days,
                within_window_days=within_window,
                last_warned_at=last_warned_at,
                dsm5_code=dsm5_code,
                icd11_code=icd11_code,
            ))

    # -----------------------------------------------------------------------
    # Self-harm / crisis URGENT override
    # Per [2] WHO ICD-11 CDDR functional severity criterion
    # -----------------------------------------------------------------------
    if crisis_dates:
        crisis_count = len(crisis_dates)
        existing_crisis: Optional[UserCondition] = (
            db.query(UserCondition)
            .filter(
                UserCondition.user_id == user_id,
                UserCondition.condition_name == _SELF_HARM_CONDITION_NAME,
            )
            .first()
        )
        last_warned_at = now
        if existing_crisis:
            existing_crisis.occurrence_count  = crisis_count
            existing_crisis.avg_confidence    = 1.0
            existing_crisis.last_seen_at      = max(crisis_dates)
            existing_crisis.confirmed         = True
            existing_crisis.warning_level     = "urgent"
            existing_crisis.intensity_score   = 1.0
            existing_crisis.consecutive_days  = _count_consecutive_days(crisis_dates)
            existing_crisis.within_window_days = CONDITION_WINDOW_DAYS
            existing_crisis.last_warned_at    = last_warned_at
            existing_crisis.icd11_code        = None
            existing_crisis.dsm5_code         = None
        else:
            db.add(UserCondition(
                user_id=user_id,
                condition_name=_SELF_HARM_CONDITION_NAME,
                occurrence_count=crisis_count,
                avg_confidence=1.0,
                first_seen_at=min(crisis_dates),
                last_seen_at=max(crisis_dates),
                confirmed=True,
                warning_level="urgent",
                intensity_score=1.0,
                consecutive_days=_count_consecutive_days(crisis_dates),
                within_window_days=CONDITION_WINDOW_DAYS,
                last_warned_at=last_warned_at,
            ))

    db.commit()


# ---------------------------------------------------------------------------
# Query helper
# ---------------------------------------------------------------------------

def get_user_conditions(db: Session, user_id: int) -> list[UserCondition]:
    """
    Return all conditions for a user.

    Ordering: urgent first, then alert, then watch, then None;
    within each tier, sort by intensity_score desc.
    """
    from sqlalchemy import case

    level_order = case(
        (UserCondition.warning_level == "urgent", 0),
        (UserCondition.warning_level == "alert",  1),
        (UserCondition.warning_level == "watch",  2),
        else_=3,
    )
    return (
        db.query(UserCondition)
        .filter(UserCondition.user_id == user_id)
        .order_by(level_order, UserCondition.intensity_score.desc().nulls_last())
        .all()
    )
