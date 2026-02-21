# FleetFlow Backend API

FastAPI + PostgreSQL backend for the FleetFlow Fleet & Logistics Management System.

## Setup

### 1. Clone & create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your actual values
```

### 3. Run locally
```bash
uvicorn main:app --reload
```

API docs available at: http://localhost:8000/docs

---

## Deployment (Railway / Render)

Set the following environment variables on your hosting platform:

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `SECRET_KEY` | Strong random string for JWT signing |
| `FRONTEND_URL` | Your production frontend URL |
| `ENVIRONMENT` | Set to `production` |
| `ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | e.g. `60` |

> **Never commit `.env` to version control.** Use `.env.example` as a reference.

The `Procfile` is already configured:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

## Generating a secure SECRET_KEY

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```
