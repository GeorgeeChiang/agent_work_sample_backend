# 借書系統 Backend

FastAPI + PostgreSQL 的借書系統範例後端。

## Demo 帳號

| 帳號 | 密碼 | 使用者 |
|---|---|---|
| user1 | 123456 | 小明 |
| user2 | 123456 | 小華 |
| user3 | 123456 | 小美 |

## API

| Method | Path | 說明 |
|---|---|---|
| GET | `/health` | 健康檢查 |
| POST | `/auth/login` | 登入 |
| GET | `/books` | 取得書籍與借閱狀態 |
| GET | `/users` | 取得使用者 |
| POST | `/loans` | 借書 |
| POST | `/loans/{book_id}/return` | 還書 |

## Local Docker

此 repo 通常由 `agent_workflow_system/docker-compose.yml` 一起啟動。

