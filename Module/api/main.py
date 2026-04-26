import sys
import os

# Đảm bảo import được src/ và inference.py từ thư mục Module-1/
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import analyze, assess
from api.services.module1 import get_predictor
from api.services.module2 import get_predictor as get_m2_predictor

app = FastAPI(
    title="NhatKi AI Service",
    description="Module-1: Emotion & Hate Speech Detection | Module-2: Mental Health Assessment",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze.router)
app.include_router(assess.router)


@app.on_event("startup")
async def startup():
    """Pre-load cả hai model khi server khởi động để request đầu tiên không bị chậm."""
    get_predictor()       # Module-1: EmotionHatePredictor
    get_m2_predictor()    # Module-2: MentalHealthPredictor


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "NhatKi AI Service đang hoạt động"}
