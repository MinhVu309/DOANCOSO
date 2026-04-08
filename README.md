# NhatKi — Ứng dụng Nhật Ký Tâm An

Ứng dụng nhật ký cá nhân với tính năng phân tích cảm xúc bằng AI, giúp người dùng theo dõi tâm trạng và sức khỏe tinh thần mỗi ngày.

---

## Tổng quan dự án

```
NhatKi/
├── client/              # Frontend — React + Tailwind CSS
├── backend/             # Backend  — FastAPI + SQLAlchemy
└── docker-compose.yml   # PostgreSQL database
```

---

## Tính năng

| Trang | Mô tả |
|---|---|
| **Journaling** | Viết nhật ký, gắn tag cảm xúc, phân tích sentiment bằng AI |
| **History** | Xem lại các bài nhật ký theo ngày/tháng |
| **Trends** | Biểu đồ tâm trạng, chỉ số căng thẳng/lo âu, streak viết |
| **Categories** | Quản lý danh mục nhật ký |
| **Settings** | Cài đặt tài khoản, thông báo, giao diện, bảo mật |

---

## Tech Stack

### Frontend
- **React 19** + React Router DOM
- **Tailwind CSS** — giao diện Material Design 3
- **Material Symbols** — icon set

### Backend
- **FastAPI** — REST API
- **SQLAlchemy 2** + **Alembic** — ORM và migrations
- **PostgreSQL** — database (chạy qua Docker)
- **bcrypt** — hash mật khẩu
- **python-jose** — JWT authentication

### Infrastructure
- **Docker** + **docker-compose** — chạy PostgreSQL
- **DBeaver** — quản lý database

---

## Cài đặt & Chạy

### Yêu cầu
- Node.js >= 18
- Python >= 3.10
- Docker Desktop

---

### 1. Khởi động Database

```bash
# Tại thư mục gốc NhatKi/
docker-compose up -d
```

PostgreSQL sẽ chạy tại `localhost:5432`.

---

### 2. Backend

```bash
cd backend

# Tạo môi trường ảo
python3 -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows

# Cài dependencies
pip install -r requirements.txt

# Cấu hình môi trường
cp .env.example .env
# Mở .env và thay SECRET_KEY bằng key thật:
# python3 -c "import secrets; print(secrets.token_hex(32))"

# Chạy server
uvicorn app.main:app --reload
```

Backend chạy tại: http://localhost:8000
Swagger UI: http://localhost:8000/docs

---

### 3. Frontend

```bash
cd client

# Cài dependencies
npm install

# Chạy dev server
npm start
```

Frontend chạy tại: http://localhost:3000

---

## Kết nối DBeaver

Vào DBeaver → **New Connection** → **PostgreSQL** → điền thông tin:

| Trường | Giá trị |
|---|---|
| Host | `localhost` |
| Port | `5432` |
| Database | `nhatki` |
| Username | `nhatki` |
| Password | `nhatki123` |

---

## API Endpoints

### Auth

| Method | Endpoint | Mô tả |
|---|---|---|
| POST | `/api/auth/register` | Đăng ký tài khoản |
| POST | `/api/auth/login` | Đăng nhập, trả về JWT |
| GET | `/api/auth/me` | Lấy thông tin user hiện tại |

#### Ví dụ đăng ký
```json
POST /api/auth/register
{
  "email": "user@example.com",
  "username": "nguyen_van_a",
  "password": "matkhau123",
  "display_name": "Nguyễn Văn A"
}
```

#### Ví dụ đăng nhập
```json
POST /api/auth/login
{
  "email": "user@example.com",
  "password": "matkhau123"
}
```

---

## Bảo mật

- Mật khẩu được hash bằng **bcrypt** với salt tự động
- JWT token ký bằng **HS256**, hết hạn sau 24 giờ
- Timing-safe authentication — tránh timing attack khi sai email
- Validation đầu vào qua **Pydantic**

---

## Database Migrations (Alembic)

```bash
cd backend
source venv/bin/activate

# Tạo migration mới
alembic revision --autogenerate -m "tên migration"

# Chạy migration
alembic upgrade head

# Rollback
alembic downgrade -1
```
