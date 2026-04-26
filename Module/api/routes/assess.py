from fastapi import APIRouter
from pydantic import BaseModel, Field

from api.services.module2 import assess

router = APIRouter(prefix="/api", tags=["Assess"])


class AssessRequest(BaseModel):
    text: str = Field(..., min_length=1)
    emotions: list[str]
    hate_speech: str


class ConditionScore(BaseModel):
    label: str
    confidence: float


class AssessResponse(BaseModel):
    condition: str
    confidence: float
    severity: str | None = None
    conditions: list[ConditionScore]


@router.post("/assess", response_model=AssessResponse)
async def assess_mental_health(body: AssessRequest):
    """
    API 2: Nhận text đã qua filter Module-1, chạy Module-2 dự đoán sức khỏe tâm thần.
    Endpoint này không nên gọi trực tiếp từ web — chỉ dùng nội bộ hoặc từ /api/analyze.
    """
    result = await assess(
        text=body.text,
        emotions=body.emotions,
        hate_speech=body.hate_speech,
    )
    return AssessResponse(**result)
