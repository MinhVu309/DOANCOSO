import asyncio
import logging

from fastapi import APIRouter
from pydantic import BaseModel, Field

from api.services import module1
from api.services.module2 import assess

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["Analyze"])


class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)


class LabelScore(BaseModel):
    label: str
    confidence: float


class ConditionScore(BaseModel):
    label: str
    confidence: float


class AssessmentResult(BaseModel):
    condition: str
    confidence: float
    severity: str | None = None
    conditions: list[ConditionScore]


class AnalyzeResponse(BaseModel):
    original_text: str
    cleaned_text: str
    # Multi-label emotions (28 nhan ViGoEmotions, score > per-label threshold)
    emotions: list[str]
    emotion_scores: list[LabelScore]
    # Hate speech
    hate: str
    hate_score: float
    # Backward-compat aliases (backend doc cu dung)
    hate_speech: str
    hate_confidence: float
    # Triggered emotions + assessment flag
    triggered_emotions: list[str] = []
    needs_assessment: bool
    assessment: AssessmentResult | None = None


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_text(body: AnalyzeRequest):
    """
    Nhan text, chay Module-1 phan tich emotion (28 nhan, multi-label) + hate speech.
    Neu co nhan cam xuc ngoai safe set hoac hate != Clean -> goi Module-2.
    """
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, module1.analyze, body.text)

    assessment = None
    if result['needs_assessment']:
        try:
            assessment = await assess(
                text=result['original_text'],
                emotions=result['triggered_emotions'],
                hate_speech=result['hate'],
            )
        except Exception as e:
            logger.warning("Module-2 assessment failed: %s", e)

    return AnalyzeResponse(**result, assessment=assessment)
