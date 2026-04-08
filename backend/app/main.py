from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .routers import auth

# Tạo bảng tự động (dùng cho dev với SQLite)
# Khi dùng Alembic migrations thì bỏ dòng này
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NhatKi API",
    description="Backend cho ứng dụng nhật ký",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "NhatKi API đang hoạt động"}
