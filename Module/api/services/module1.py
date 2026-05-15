"""
Singleton wrapper cho EmotionHatePredictor (Module-1 ver 2.6 — 28 nhãn ViGoEmotions).
Load model một lần duy nhất khi startup, tái sử dụng cho mọi request.
"""

import os
from functools import lru_cache

from inference import EmotionHatePredictor

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # Module/

MODEL_PATH     = os.path.join(BASE_DIR, 'Model', 'best_multitask_model.pth')
THRESHOLD_PATH = os.path.join(BASE_DIR, 'Model', 'emotion_thresholds.json')
DICT_PATH      = os.path.join(BASE_DIR, 'data', 'Xử lý teencode.xlsx')

# Tích cực + Nhận thức + Trung lập — không trigger Module-2
# Chỉ nhóm Tiêu cực (fear, nervousness, remorse, embarrassment,
# disappointment, sadness, grief, disgust, anger, annoyance, disapproval)
# mới gọi Module-2 (theo Bảng 3 ViGoEmotions).
SAFE_EMOTIONS = {
    # Tích cực
    'amusement', 'excitement', 'joy', 'love', 'desire', 'optimism',
    'caring', 'pride', 'admiration', 'gratitude', 'relief', 'approval',
    # Nhận thức
    'realization', 'surprise', 'curiosity', 'confusion',
    # Trung lập
    'neutral',
}
SAFE_HATE_LABEL = 'Clean'


@lru_cache(maxsize=1)
def get_predictor() -> EmotionHatePredictor:
    """Trả về instance duy nhất của predictor (lazy-load)."""
    return EmotionHatePredictor(
        model_path=MODEL_PATH,
        threshold_path=THRESHOLD_PATH,
        dict_path=DICT_PATH,
    )


def analyze(text: str) -> dict:
    """
    Chạy Module-1, tính triggered_emotions và needs_assessment.

    triggered_emotions: nhãn cảm xúc được dự đoán VÀ không thuộc SAFE_EMOTIONS
                        — đây là tín hiệu cần chuyển sang Module-2.
    needs_assessment:   True khi có triggered emotion HOẶC hate speech != Clean.
    """
    result = get_predictor().predict(text)
    triggered = [e for e in result['emotions'] if e not in SAFE_EMOTIONS]
    result['triggered_emotions'] = triggered
    result['needs_assessment'] = bool(triggered) or result['hate'] != SAFE_HATE_LABEL
    return result
