# NhatKi — Ứng dụng Nhật Ký Tâm An

Ứng dụng nhật ký cá nhân với tính năng phân tích cảm xúc bằng AI, giúp người dùng theo dõi tâm trạng và sức khỏe tinh thần mỗi ngày.

---

## Kiến trúc tổng quan

```
NhatKi/
├── client/              # Frontend  — React 19 + Tailwind CSS     :3000
├── backend/             # Backend   — FastAPI + PostgreSQL         :8000
├── Module-1/            # AI Service — PhoBERT multitask          :8001
└── docker-compose.yml   # PostgreSQL 16
```

```
Frontend (React :3000)
    ↕ REST + JWT
Backend (FastAPI :8000)   — auth, entries, categories, trends, users
    ↕ HTTP (httpx)
Module-1 AI (FastAPI :8001) — emotion (7 nhãn) + hate speech (3 nhãn)
    ↕ stub
Module-2 (chưa có)         — đánh giá chuyên sâu
```

---

## Tính năng

| Trang | Mô tả |
|---|---|
| **Đăng nhập / Đăng ký** | JWT auth, form validation |
| **Journaling** | Viết nhật ký, gắn tag, chọn danh mục, phân tích AI real-time |
| **History** | Xem lại nhật ký nhóm theo tháng, hiển thị kết quả AI |
| **Trends** | Biểu đồ tâm trạng, streak viết, chỉ số tinh thần, cảm xúc phổ biến |
| **Categories** | Tạo/xóa danh mục với icon và màu sắc tuỳ chỉnh |
| **Settings** | Profile, avatar upload, nhắc nhở, giao diện |

---

## Tech Stack

### Frontend
- **React 19** + React Router DOM 7
- **Tailwind CSS** — Material Design 3 theme
- **Axios** — HTTP client với auto JWT injection
- **Material Symbols** — icon set

### Backend
- **FastAPI** — REST API, async
- **SQLAlchemy 2** + **Alembic** — ORM & migrations
- **PostgreSQL 16** — database (Docker)
- **bcrypt** + **python-jose** — password hashing & JWT
- **httpx** — async HTTP client gọi Module-1

### AI Service (Module-1)
- **PhoBERT** (`vinai/phobert-base`) — Vietnamese NLP
- **PyTorch** — multitask model (emotion + hate speech)
- **FastAPI** — service wrapper

### Infrastructure
- **Docker** + **docker-compose** — PostgreSQL

---

## Cài đặt & Chạy

### Yêu cầu
- Node.js >= 18
- Python >= 3.10
- Docker Desktop

### 1. Khởi động Database

```bash
# Tại thư mục gốc NhatKi/
docker-compose up -d
```

PostgreSQL chạy tại `localhost:5432`.

### 2. Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # macOS/Linux

pip install -r requirements.txt

# Tạo .env (nếu chưa có)
cat > .env << 'EOF'
DATABASE_URL=postgresql://nhatki:nhatki123@localhost:5432/nhatki
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
EOF

# Chạy migrations
alembic upgrade head

# (Tùy chọn) Seed data mẫu
python -m app.seed

# Chạy server
uvicorn app.main:app --reload
```

Backend: http://localhost:8000 | Swagger: http://localhost:8000/docs

### 3. Module-1 AI Service

> Bắt buộc có file `Module-1/Model/best_multitask_model.pth` (không commit vào repo).

```bash
cd Module-1
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

# Phải chạy từ thư mục Module-1/
uvicorn api.main:app --reload --port 8001
```

Module-1: http://localhost:8001 | Swagger: http://localhost:8001/docs

### 4. Frontend

```bash
cd client
npm install
npm start
```

Frontend: http://localhost:3000

---

## Tài khoản test (sau khi seed)

```
Email:    test@nhatki.app
Password: test123
```

---

## API Endpoints

### Auth (`:8000`)

| Method | Endpoint | Auth | Mô tả |
|---|---|---|---|
| POST | `/api/auth/register` | — | Đăng ký |
| POST | `/api/auth/login` | — | Đăng nhập → JWT |
| GET | `/api/auth/me` | Bearer | Thông tin user |

### Entries (`:8000`)

| Method | Endpoint | Mô tả |
|---|---|---|
| GET | `/api/entries` | Danh sách (filter: date, category, tag, grouped) |
| POST | `/api/entries` | Tạo nhật ký mới |
| GET | `/api/entries/{id}` | Chi tiết |
| PUT | `/api/entries/{id}` | Cập nhật |
| DELETE | `/api/entries/{id}` | Xóa |
| POST | `/api/entries/{id}/analyze` | Trigger AI phân tích |
| GET | `/api/entries/{id}/analysis` | Xem kết quả phân tích |

### Categories (`:8000`)

| Method | Endpoint | Mô tả |
|---|---|---|
| GET | `/api/categories` | Danh sách + entry_count |
| POST | `/api/categories` | Tạo mới |
| PUT | `/api/categories/{id}` | Cập nhật |
| DELETE | `/api/categories/{id}` | Xóa |

### Trends (`:8000`)

| Method | Endpoint | Mô tả |
|---|---|---|
| GET | `/api/trends/mood-chart?period=week\|month` | Biểu đồ tâm trạng |
| GET | `/api/trends/streak` | Streak & tổng entries |
| GET | `/api/trends/mental-index?period=month` | Chỉ số tinh thần |
| GET | `/api/trends/top-emotions?period=week` | Cảm xúc phổ biến |

### Users (`:8000`)

| Method | Endpoint | Mô tả |
|---|---|---|
| GET | `/api/users/me/profile` | Hồ sơ |
| PUT | `/api/users/me/profile` | Cập nhật hồ sơ |
| POST | `/api/users/me/avatar` | Upload avatar |
| DELETE | `/api/users/me/avatar` | Xóa avatar |
| GET | `/api/users/me/preferences` | Tùy chọn |
| PUT | `/api/users/me/preferences` | Cập nhật tùy chọn |

### AI Analyze (`:8001`)

| Method | Endpoint | Mô tả |
|---|---|---|
| POST | `/api/analyze` | Phân tích emotion + hate speech |
| POST | `/api/assess` | Gọi Module-2 trực tiếp |

---

## Database Schema

```
users
  └─ entries        (user_id FK)
       ├─ entry_tags        (entry_id FK)
       └─ analysis_results  (entry_id FK, unique)
  └─ categories     (user_id FK)
  └─ user_preferences (user_id FK, unique)
```

### Emotion labels
`Anger · Disgust · Enjoyment · Fear · Other · Sadness · Surprise`

### Hate speech labels
`Clean · Offensive · Hate`

---

## Database Migrations

```bash
cd backend
source venv/bin/activate

alembic revision --autogenerate -m "tên migration"
alembic upgrade head
alembic downgrade -1
```

---

## Bảo mật

- Mật khẩu hash bằng **bcrypt** với salt tự động
- JWT **HS256**, hết hạn sau 24 giờ
- Timing-safe auth — tránh user enumeration
- Ownership check trên mọi query (không lộ data user khác)
- Upload giới hạn 5MB, chỉ chấp nhận JPG/PNG/WEBP

---

## Kết nối DBeaver

| Trường | Giá trị |
|---|---|
| Host | `localhost` |
| Port | `5432` |
| Database | `nhatki` |
| Username | `nhatki` |
| Password | `nhatki123` |
