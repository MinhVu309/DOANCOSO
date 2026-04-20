"""
HTTP client gọi Module-2.
Hiện tại trả stub response — thay MODULE2_URL khi Module-2 sẵn sàng.
"""

import os
import httpx

MODULE2_URL = os.getenv("MODULE2_URL", "")  # VD: http://localhost:8002


async def assess(text: str, emotion: str, hate_speech: str) -> dict | None:
    """
    Gọi Module-2 để dự đoán tình trạng sức khỏe tâm thần.
    Trả về dict { condition, confidence, severity } hoặc None nếu chưa có Module-2.
    """
    if not MODULE2_URL:
        # Module-2 chưa được deploy → trả stub để không block API 1
        return {
            "condition": "Pending",
            "confidence": 0.0,
            "severity": None,
        }

    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = client.post(
            f"{MODULE2_URL}/predict",
            json={"text": text, "emotion": emotion, "hate_speech": hate_speech},
        )
        resp.raise_for_status()
        return resp.json()
