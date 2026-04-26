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


@lru_cache(maxsize=1)
def get_predictor() -> MentalHealthPredictor:
    """Trả về instance duy nhất của Module-2 predictor (lazy-load)."""
    return MentalHealthPredictor(
        model_path=MODEL_PATH,
        label_path=LABEL_PATH,
        dict_path=DICT_PATH,
    )


async def assess(text: str, emotions: list[str], hate_speech: str) -> dict:
    """
    Chay Module-2 du doan tinh trang suc khoe tam than tu text.
    emotions: danh sach nhan cam xuc co confidence > 0.3 tu Module-1.
    Tra ve dict { condition, confidence, severity, conditions }.
    PyTorch inference chay trong thread pool de khong block event loop.
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: get_predictor().predict(text, top_k=5))
