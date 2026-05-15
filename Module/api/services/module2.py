"""
Singleton wrapper cho MentalHealthPredictor (Module-2).
Load model một lần duy nhất khi startup, tái sử dụng cho mọi request.
"""

import asyncio
import os
from functools import lru_cache

from inference_module2 import MentalHealthPredictor

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # Module/

MODEL_PATH = os.path.join(BASE_DIR, 'Model', 'best_mental_health_multilabel.pth')
LABEL_PATH = os.path.join(BASE_DIR, 'Model', 'label_names.pkl')
DICT_PATH  = os.path.join(BASE_DIR, 'data', 'Xử lý teencode.xlsx')

# Trong so tinh severity tu nhan Module-1 (28 nhan ViGoEmotions)
_EMOTION_WEIGHT: dict[str, int] = {
    # Cao — lien quan truc tiep den benh ly tam than
    "sadness": 2, "grief": 2, "fear": 2, "nervousness": 2,
    # Trung binh
    "remorse": 1, "embarrassment": 1, "disappointment": 1,
    "disgust": 1, "anger": 1, "annoyance": 1, "disapproval": 1,
    "confusion": 1,
    # Trung tinh / nhe
    "realization": 0, "surprise": 0, "curiosity": 0,
    # Tich cuc (weight = 0)
    "amusement": 0, "excitement": 0, "joy": 0, "love": 0,
    "desire": 0, "optimism": 0, "caring": 0, "pride": 0,
    "admiration": 0, "gratitude": 0, "relief": 0, "approval": 0,
    "neutral": 0,
}
_HATE_WEIGHT: dict[str, int] = {
    "Hate": 3,
    "Offensive": 1,
    "Clean": 0,
}


@lru_cache(maxsize=1)
def get_predictor() -> MentalHealthPredictor:
    """Trả về instance duy nhất của Module-2 predictor (lazy-load)."""
    return MentalHealthPredictor(
        model_path=MODEL_PATH,
        label_path=LABEL_PATH,
        dict_path=DICT_PATH,
    )


def _build_augmented_text(text: str, emotions: list[str], hate_speech: str) -> str:
    """Prepend nhãn Module-1 vào text để model có thêm context."""
    parts = []
    if emotions:
        parts.append(f"[CẢM XÚC: {', '.join(emotions)}]")
    if hate_speech and hate_speech != "Clean":
        parts.append(f"[{hate_speech}]")
    return " ".join(parts + [text]) if parts else text


def _compute_severity(emotions: list[str], hate_speech: str, top_confidence: float) -> str:
    """Tính severity dựa trên nhãn Module-1 và confidence của Module-2."""
    score = sum(_EMOTION_WEIGHT.get(e, 0) for e in emotions)
    score += _HATE_WEIGHT.get(hate_speech, 0)
    if top_confidence > 0.7:
        score += 2
    if score >= 5:
        return "High"
    if score >= 2:
        return "Medium"
    return "Low"


async def assess(text: str, emotions: list[str], hate_speech: str) -> dict:
    """
    Chạy Module-2 dự đoán tình trạng sức khỏe tâm thần.
    - emotions: danh sách nhãn cảm xúc có confidence > 0.3 từ Module-1.
    - hate_speech: nhãn hate speech top-1 từ Module-1.
    - Text được augment với nhãn Module-1 trước khi đưa vào model.
    - Severity được tính rule-based từ nhãn Module-1 + confidence Module-2.
    Trả về dict { condition, confidence, severity, conditions }.
    """
    augmented = _build_augmented_text(text, emotions, hate_speech)
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, lambda: get_predictor().predict(augmented, top_k=5))
    result["severity"] = _compute_severity(emotions, hate_speech, result["confidence"])
    return result
