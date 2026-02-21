# FleetFlow Frontend

React + Tailwind CSS frontend for the FleetFlow fleet management system.

## Setup

```bash
npm install
cp .env.example .env
# Edit .env — set VITE_API_URL to your deployed backend URL
npm run dev
```

## Deploy (Netlify / Vercel / Railway)

```bash
npm run build
# Upload the dist/ folder, or connect your GitHub repo
```

**Environment variable to set on your host:**
```
VITE_API_URL=https://your-backend.railway.app/api/v1
```

## Pages

| Route | Description |
|---|---|
| `/login` | Authentication |
| `/` | Dashboard with stats + alerts |
| `/vehicles` | Vehicle management |
| `/drivers` | Driver management |
| `/trips` | Trip creation, dispatch, complete, cancel |
| `/fuel` | Fuel log entries |
| `/maintenance` | Maintenance tracking |
| `/expenses` | Expense logging |

## Roles

The UI respects backend roles — forms that require `fleet_manager` or `dispatcher` will fail gracefully with error messages from the API if the user lacks the role.


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
