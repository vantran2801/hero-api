# Heroes API

Heroes API là ứng dụng REST xây dựng bằng FastAPI, SQLModel và SQLite hoặc
PostgreSQL. Ứng dụng quản lý heroes, teams và missions, bao gồm quan hệ nhiều
nhiều giữa heroes và missions.

Project cũng có một trang frontend đơn giản để gọi API bằng Fetch, cấu hình CORS
cho môi trường phát triển và bộ kiểm thử bằng pytest với SQLite in-memory.

## Tính năng

- CRUD heroes với phân trang và bộ lọc theo tuổi, team và tên.
- Tạo team và xem danh sách heroes thuộc một team.
- Tạo mission, gán mission cho hero và xem missions của hero.
- Validation dữ liệu bằng Pydantic/SQLModel.
- Trạng thái hero `active` hoặc `retired`.
- Tự động lưu thời điểm tạo hero qua trường `created_at`.
- Tài liệu API tại Swagger UI và ReDoc.
- Migration cơ sở dữ liệu bằng Alembic.
- Frontend mẫu tại `frontend/index.html`.

## Yêu cầu

- Python 3.10 trở lên.
- pip.
- PostgreSQL là tùy chọn. Nếu không cấu hình PostgreSQL, ứng dụng sử dụng
  SQLite tại `app.db`.
- Live Server hoặc một HTTP server bất kỳ nếu muốn chạy frontend.

## Cài đặt

Mở terminal tại thư mục project:

```powershell
cd C:\Users\TNC\Downloads\hero-api\hero-api
```

Tạo và kích hoạt virtual environment trên Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Nếu PowerShell chặn việc chạy script, chỉ áp dụng chính sách cho user hiện tại:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Cài dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Cấu hình

Mặc định ứng dụng sử dụng SQLite:

```text
sqlite:///./app.db
```

Có thể tạo file `.env` từ `.env.example`, sau đó thiết lập các biến môi trường
trong terminal. Ứng dụng hiện đọc trực tiếp biến môi trường của hệ thống.

Ví dụ dùng SQLite:

```powershell
$env:DATABASE_URL = "sqlite:///./app.db"
$env:CORS_ORIGINS = "http://localhost:5500,http://127.0.0.1:5500"
```

Ví dụ dùng PostgreSQL:

```powershell
$env:DATABASE_URL = "postgresql+psycopg://user:password@localhost:5432/appdb"
$env:CORS_ORIGINS = "http://localhost:5500,http://127.0.0.1:5500"
```

Không đưa file `.env`, mật khẩu hoặc thông tin kết nối thật vào Git. File
`.env.example` chỉ dùng làm mẫu cấu hình.

## Khởi tạo cơ sở dữ liệu

Chạy migration:

```powershell
python -m alembic upgrade head
```

Tạo dữ liệu mẫu:

```powershell
python -m app.seed
```

Lệnh seed an toàn khi chạy nhiều lần; nếu database đã có team, lệnh sẽ không
thêm dữ liệu trùng.

## Chạy API

```powershell
fastapi dev app/main.py
```

Các địa chỉ quan trọng:

- API: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

Tất cả endpoint nghiệp vụ sử dụng prefix `/api/v1`.

## Chạy frontend

API phải đang chạy trước khi mở frontend. Có thể dùng Live Server trong VS Code
với thư mục `frontend`, hoặc chạy HTTP server bằng Python:

```powershell
python -m http.server 5500 --directory frontend
```

Mở `http://127.0.0.1:5500` trên trình duyệt. Frontend hỗ trợ tải danh sách
heroes, tải teams vào dropdown và tạo hero mới.

## Chạy test

Các test sử dụng SQLite in-memory nên không thay đổi dữ liệu trong `app.db`:

```powershell
python -m pytest -v
```

## API chính

| Method | Endpoint | Mô tả |
| --- | --- | --- |
| POST | `/api/v1/heroes` | Tạo hero |
| GET | `/api/v1/heroes` | Danh sách heroes, hỗ trợ `offset`, `limit`, `min_age`, `team_id`, `name` |
| GET | `/api/v1/heroes/{hero_id}` | Xem một hero |
| PATCH | `/api/v1/heroes/{hero_id}` | Cập nhật một phần hero |
| DELETE | `/api/v1/heroes/{hero_id}` | Xóa hero |
| POST | `/api/v1/teams` | Tạo team |
| GET | `/api/v1/teams` | Danh sách teams |
| GET | `/api/v1/teams/{team_id}/heroes` | Heroes của một team |
| POST | `/api/v1/missions` | Tạo mission |
| POST | `/api/v1/heroes/{hero_id}/missions/{mission_id}` | Gán mission cho hero |
| GET | `/api/v1/heroes/{hero_id}/missions` | Missions của hero |

Ví dụ tạo team:

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://127.0.0.1:8000/api/v1/teams `
  -ContentType "application/json" `
  -Body '{"name":"Avengers","headquarters":"New York"}'
```

Ví dụ tạo hero:

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://127.0.0.1:8000/api/v1/heroes `
  -ContentType "application/json" `
  -Body '{"name":"Tony","age":45,"power":"powered armor","secret_name":"Iron Man","team_id":1}'
```

## Cấu trúc thư mục

```text
hero-api/
├── app/
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── seed.py
│   └── routers/
│       ├── heros.py
│       ├── mission.py
│       └── teams.py
├── frontend/
│   └── index.html
├── migrations/
│   └── versions/
├── tests/
│   ├── conftest.py
│   └── test_api.py
├── .env.example
├── .gitignore
├── alembic.ini
└── requirements.txt
```

## Migration khi thay đổi model

Sau khi thay đổi model, tạo migration mới:

```powershell
python -m alembic revision --autogenerate -m "describe the change"
python -m alembic upgrade head
```

Luôn kiểm tra file migration trước khi chạy trên database thật.
