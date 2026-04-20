import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import settings
from .database import engine, Base
from .routers import auth, entries, categories, trends, users

# Tạo bảng tự động (dùng cho dev)
# Khi Alembic ổn định thì bỏ dòng này
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NhatKi API",
    description="Backend cho ứng dụng nhật ký",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files cho uploads
os.makedirs(os.path.join(settings.upload_dir, "avatars"), exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")

app.include_router(auth.router)
app.include_router(entries.router)
app.include_router(categories.router)
app.include_router(trends.router)
app.include_router(users.router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "NhatKi API đang hoạt động"}
