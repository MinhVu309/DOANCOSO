"""
Singleton wrapper cho EmotionHatePredictor.
Load model một lần duy nhất khi startup, tái sử dụng cho mọi request.
"""

import os
from functools import lru_cache

from inference import EmotionHatePredictor

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # Module-1/

MODEL_PATH = os.path.join(BASE_DIR, 'Model', 'best_multitask_model.pth')
DICT_PATH  = os.path.join(BASE_DIR, 'data', 'Xử lý teencode.xlsx')

# Nhãn được coi là "bình thường", không cần gửi sang Module-2
SAFE_EMOTIONS    = {'Enjoyment', 'Other'}
SAFE_HATE_LABEL  = 'Clean'
EMOTION_THRESHOLD = 0.3


@lru_cache(maxsize=1)
def get_predictor() -> EmotionHatePredictor:
    """Trả về instance duy nhất của predictor (lazy-load)."""
    return EmotionHatePredictor(model_path=MODEL_PATH, dict_path=DICT_PATH)


def get_triggered_emotions(emotion_scores: list[dict]) -> list[str]:
    """
    Trả về danh sách nhãn cảm xúc có confidence > EMOTION_THRESHOLD
    và KHÔNG thuộc SAFE_EMOTIONS — đây là các nhãn cần gửi sang Module-2.
    """
    return [
        s["label"] for s in emotion_scores
        if s["confidence"] > EMOTION_THRESHOLD and s["label"] not in SAFE_EMOTIONS
    ]


def analyze(text: str) -> dict:
    """
    Chạy Module-1, tính triggered_emotions và needs_assessment.
    """
    result = get_predictor().predict(text)
    triggered = get_triggered_emotions(result['emotion_scores'])
    result['triggered_emotions'] = triggered
    # Cần đánh giá thêm nếu có nhãn cảm xúc vượt ngưỡng HOẶC hate speech != Clean
    result['needs_assessment'] = bool(triggered) or result['hate_speech'] != SAFE_HATE_LABEL
    return result
