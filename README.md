# NhatKi — Ứng dụng Nhật Ký Tâm An

Ứng dụng nhật ký cá nhân với tính năng phân tích cảm xúc và đánh giá sức khỏe tâm thần bằng AI, giúp người dùng theo dõi tâm trạng mỗi ngày.

---

## Kiến trúc tổng quan

```
NhatKi/
├── client/              # Frontend  — React 19 + Tailwind CSS        :3000
├── backend/             # Backend   — FastAPI + PostgreSQL            :8000
├── Module/              # AI Service — Module-1 + Module-2 (PhoBERT) :8001
└── docker-compose.yml   # PostgreSQL 16
```

```
Frontend (React :3000)
    ↕ REST + JWT
Backend (FastAPI :8000)      — auth, entries, categories, trends, admin, users
    ↕ HTTP (httpx)
Module AI (FastAPI :8001)
    ├── Module-1             — emotion (28 nhãn ViGoEmotions) + hate speech (3 nhãn)
    └── Module-2             — đánh giá 58 tình trạng sức khỏe tâm thần
```

**Luồng xử lý:**

```
Người dùng viết nhật ký
    → POST /api/entries/{id}/analyze       (Backend :8000)
    → POST /api/analyze                    (Module AI :8001)
         → Module-1: emotion (7 nhãn) + hate speech (3 nhãn)
              → Lọc triggered_emotions: confidence > 0.3, ngoài {Enjoyment, Other}
         → Module-2: top-5 / 58 tình trạng tâm thần  (chỉ khi needs_assessment=True)
    ← Lưu analysis_results vào DB
    → aggregate_user_conditions()          (Backend, chạy ngay sau)
         → Đếm conditions 30 ngày gần nhất
         → confirmed=True khi xuất hiện >= 3 lần
    ← Kết quả hiển thị trên Trends
```

> Chi tiết đầy đủ về AI pipeline: [Module/AI_PIPELINE.md](Module/AI_PIPELINE.md)

---

## Tính năng

| Trang | Mô tả |
|---|---|
| **Đăng nhập / Đăng ký** | JWT auth, form validation |
| **Journaling** | Viết nhật ký, gắn tag, chọn danh mục, phân tích AI real-time |
| **History** | Xem lại nhật ký nhóm theo tháng, hiển thị kết quả AI |
| **Trends** | Biểu đồ tâm trạng, streak viết, chỉ số tinh thần, cảm xúc phổ biến, cảnh báo sức khỏe tâm thần (DSM-5/ICD-11) |
| **Categories** | Tạo/xóa danh mục với icon và màu sắc tuỳ chỉnh |
| **Settings** | Profile, avatar upload, nhắc nhở, giao diện |
| **Admin Dashboard** | Thống kê nền tảng, quản lý user, kích hoạt/vô hiệu hóa tài khoản (role=admin) |

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
- **httpx** — async HTTP client gọi Module AI

### AI Service (`Module/`)
- **PhoBERT** (`vinai/phobert-base-v2`) — Vietnamese NLP backbone
- **Module-1** — Multi-task model: emotion (28 label ViGoEmotions) + hate speech (3 label), per-label threshold
- **Module-2** — Multi-label model: 58 tinh trang suc khoe tam than
- **PyTorch** + **FastAPI**

### Infrastructure
- **Docker** + **docker-compose** — PostgreSQL

---

## Yêu cầu hệ thống

- Node.js >= 18
- Python >= 3.10 (khuyến nghị 3.12)
- Docker Desktop

### File model (không commit vào repo)

Đặt vào `Module/Model/`:
```
Module/Model/
├── best_multitask_model.pth          # Module-1 (~517MB)
├── best_mental_health_multilabel.pth # Module-2 (~516MB)
├── label_names.pkl                   # 58 label tinh trang tam than
└── emotion_thresholds.json           # Per-label threshold 28 ViGoEmotions
```

---

## Cài đặt & Chạy

### 1. Database

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
# venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

Tạo file `backend/.env`:
```env
DATABASE_URL=postgresql://nhatki:nhatki123@localhost:5432/nhatki
SECRET_KEY=<chạy lệnh bên dưới để tạo>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

```bash
# Tạo SECRET_KEY
python3 -c "import secrets; print(secrets.token_hex(32))"

# Chạy migrations
alembic upgrade head

# Chạy server
uvicorn app.main:app --reload
```

Backend: http://localhost:8000 | Swagger: http://localhost:8000/docs

### 3. Module AI Service

> Cần có đủ 4 file model trong `Module/Model/` trước khi chạy.

```bash
cd Module
python3 -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows

pip install -r requirements.txt

# Phải chạy từ thư mục Module/
uvicorn api.main:app --reload --port 8001
```

Module AI: http://localhost:8001 | Swagger: http://localhost:8001/docs

Lần đầu khởi động sẽ mất 30–60 giây để load cả 2 model vào bộ nhớ.

### 4. Frontend

```bash
cd client
npm install
npm start
```

Frontend: http://localhost:3000

---

## Tài khoản test (sau khi seed)

```bash
# Chạy từ backend/
source venv/bin/activate && python seed_demo.py
```

```
Email:    demo@nhatki.vn
Password: Demo@123
```

> Seed script tạo entries trải rộng 30 ngày, bao phủ đủ 3 bậc cảnh báo DSM-5/ICD-11 (watch / alert / urgent) để test trang Trends.

---

## API Endpoints

### Auth (`:8000`)

| Method | Endpoint | Auth | Mô tả |
|---|---|---|---|
| POST | `/api/auth/register` | — | Đăng ký |
| POST | `/api/auth/login` | — | Đăng nhập → JWT |
| GET | `/api/auth/me` | Bearer | Thông tin user |

### Admin (`:8000`, role=admin)

| Method | Endpoint | Mô tả |
|---|---|---|
| GET | `/api/admin/stats` | Tong so user, entry, analysis + moi trong tuan |
| GET | `/api/admin/users?page&limit&search` | Danh sach tat ca user |
| PATCH | `/api/admin/users/{id}/toggle-active` | Kich hoat / vo hieu hoa tai khoan |

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
| GET | `/api/trends/mood-chart?period=week\|month` | Bieu do tam trang |
| GET | `/api/trends/streak` | Streak & tong entries |
| GET | `/api/trends/mental-index?period=month` | Chi so tinh than |
| GET | `/api/trends/top-emotions?period=week` | Cam xuc pho bien |
| GET | `/api/trends/mental-health` | Tinh trang tam than tich luy (warning_level, dsm5_code, icd11_code) |

### Users (`:8000`)

| Method | Endpoint | Mô tả |
|---|---|---|
| GET | `/api/users/me/profile` | Hồ sơ |
| PUT | `/api/users/me/profile` | Cập nhật hồ sơ |
| POST | `/api/users/me/avatar` | Upload avatar |
| DELETE | `/api/users/me/avatar` | Xóa avatar |
| GET | `/api/users/me/preferences` | Tùy chọn |
| PUT | `/api/users/me/preferences` | Cập nhật tùy chọn |

### AI Module (`:8001`)

| Method | Endpoint | Mô tả |
|---|---|---|
| POST | `/api/analyze` | Module-1 phân tích → nếu có nhãn > 0.3 tự gọi Module-2 |
| POST | `/api/assess` | Module-2 trực tiếp (nhận `emotions: list[str]`) |

**Vi du response `/api/analyze`:**
```json
{
  "emotion": "sadness",
  "emotion_confidence": 0.82,
  "hate_speech": "Clean",
  "hate_confidence": 0.91,
  "emotion_scores": [
    { "label": "sadness",      "confidence": 0.82 },
    { "label": "grief",        "confidence": 0.54 },
    { "label": "disappointment","confidence": 0.47 }
  ],
  "triggered_emotions": ["sadness", "grief"],
  "needs_assessment": true,
  "assessment": {
    "condition": "Roi loan tram cam",
    "confidence": 0.87,
    "conditions": [
      { "label": "Roi loan tram cam", "confidence": 0.87 },
      { "label": "Mat ngu",           "confidence": 0.65 },
      { "label": "Roi loan lo au",    "confidence": 0.58 }
    ]
  }
}
```

---

## Database Schema

```
users  [id, email, username, role("user"|"admin"), is_active, ...]
  └─ entries          (user_id FK)
       ├─ entry_tags          (entry_id FK)
       └─ analysis_results    (entry_id FK, unique)
  └─ categories       (user_id FK)
  └─ user_preferences (user_id FK, unique)
  └─ user_conditions  (user_id FK)
       — occurrence_count, avg_confidence, warning_level, intensity_score,
         consecutive_days, within_window_days, dsm5_code, icd11_code
```

### Emotion labels — Module-1 (28 ViGoEmotions)
`amusement · excitement · joy · love · desire · optimism · caring · pride · admiration · gratitude · relief · approval · realization · surprise · curiosity · confusion · fear · nervousness · remorse · embarrassment · disappointment · sadness · grief · disgust · anger · annoyance · disapproval · neutral`

### Hate speech labels (Module-1)
`Clean · Offensive · Hate`

### Mental health labels (Module-2)
58 tình trạng bao gồm: Rối loạn trầm cảm, Rối loạn lo âu, Mất ngủ, Căng thẳng Stress, Rối loạn lưỡng cực, PTSD, OCD, ADHD, Tâm thần phân liệt, Bệnh Alzheimer, Bệnh Parkinson...

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
