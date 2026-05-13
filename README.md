# 借書系統 Backend

這是借書系統的後端範例 repo，使用 FastAPI + PostgreSQL 實作。正式展示時通常由 `agent_workflow_system/docker-compose.yml` 透過 submodule 一起啟動。

## 技術

| 技術 | 用途 |
|---|---|
| FastAPI | 後端 API |
| SQLAlchemy | ORM |
| PostgreSQL | 資料庫 |
| Uvicorn | ASGI server |
| Docker | 容器化執行 |

## 初始資料

系統啟動時會建立 10 本書與 3 個使用者，並預設小明已借走 1 本書。

| 帳號 | 密碼 | 使用者 |
|---|---|---|
| `user1` | `123456` | 小明 |
| `user2` | `123456` | 小華 |
| `user3` | `123456` | 小美 |

## API

| Method | Path | 說明 |
|---|---|---|
| `GET` | `/health` | 健康檢查 |
| `POST` | `/auth/login` | 登入 |
| `GET` | `/books` | 查詢所有書籍與借閱狀態 |
| `GET` | `/users` | 查詢使用者 |
| `POST` | `/loans` | 借書 |
| `POST` | `/loans/{book_id}/return` | 還書 |

API 文件：

```text
http://localhost:8000/docs
```

## 本機開發

需要先有 PostgreSQL，並設定 `DATABASE_URL`：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:DATABASE_URL="postgresql+psycopg://library:library@localhost:5432/library"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Docker

此 repo 可單獨 build Docker image，但正式 demo 建議從主專案啟動：

```powershell
cd ..\agent_workflow_system
git submodule update --init --recursive
docker compose up --build
```

啟動後後端網址：

```text
http://localhost:8000
```

