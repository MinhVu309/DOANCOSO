from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from api.services import module1
from api.services.module2 import assess

router = APIRouter(prefix="/api", tags=["Analyze"])


class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)


class LabelScore(BaseModel):
    label: str
    confidence: float


class AssessmentResult(BaseModel):
    condition: str
    confidence: float
    severity: str | None = None


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
    needs_assessment: bool
    assessment: AssessmentResult | None = None


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_text(body: AnalyzeRequest):
    """
    API 1: Nhận text từ web, chạy Module-1 gắn nhãn emotion + hate speech.
    Nếu nhãn cần đánh giá thêm → tự động gọi Module-2 và trả kết quả luôn.
    """
    result = module1.analyze(body.text)

    assessment = None
    if result['needs_assessment']:
        try:
            assessment = await assess(
                text=result['original_text'],
                emotion=result['emotion'],
                hate_speech=result['hate_speech'],
            )
        except Exception:
            # Module-2 chưa có hoặc lỗi → vẫn trả kết quả Module-1
            pass

    return AnalyzeResponse(**result, assessment=assessment)
