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
SAFE_EMOTIONS   = {'Enjoyment', 'Other'}
SAFE_HATE_LABEL = 'Clean'


@lru_cache(maxsize=1)
def get_predictor() -> EmotionHatePredictor:
    """Trả về instance duy nhất của predictor (lazy-load)."""
    return EmotionHatePredictor(model_path=MODEL_PATH, dict_path=DICT_PATH)


def is_safe(emotion: str, hate_speech: str) -> bool:
    """
    Trả về True nếu văn bản bình thường, không cần đánh giá thêm.
    Điều kiện: emotion thuộc {Enjoyment, Other} VÀ hate = Clean.
    """
    return emotion in SAFE_EMOTIONS and hate_speech == SAFE_HATE_LABEL


def analyze(text: str) -> dict:
    """
    Chạy Module-1 và thêm trường needs_assessment.
    """
    result = get_predictor().predict(text)
    result['needs_assessment'] = not is_safe(result['emotion'], result['hate_speech'])
    return result
