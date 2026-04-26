import asyncio
import logging

from fastapi import APIRouter, HTTPException
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
    # Nhãn chính (top-1)
    emotion: str
    emotion_confidence: float
    hate_speech: str
    hate_confidence: float
    # Tất cả nhãn
    emotion_scores: list[LabelScore]
    hate_scores: list[LabelScore]
    # Nhãn cảm xúc có confidence > 0.3, không thuộc safe set
    triggered_emotions: list[str] = []
    needs_assessment: bool
    assessment: AssessmentResult | None = None


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_text(body: AnalyzeRequest):
    """
    API 1: Nhan text tu web, chay Module-1 gan nhan emotion + hate speech.
    Neu co nhan cam xuc > 0.3 (ngoai safe set) hoac hate != Clean
    -> tu dong goi Module-2 voi toan bo danh sach nhan do.
    """
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, module1.analyze, body.text)

    assessment = None
    if result['needs_assessment']:
        try:
            assessment = await assess(
                text=result['original_text'],
                emotions=result['triggered_emotions'],
                hate_speech=result['hate_speech'],
            )
        except Exception as e:
            logger.warning("Module-2 assessment failed: %s", e)

    return AnalyzeResponse(**result, assessment=assessment)
