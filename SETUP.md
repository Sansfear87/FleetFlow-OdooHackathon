# FleetFlow — Setup Guide

## What's in this ZIP

```
fleetflow/
├── backend/          ← FastAPI Python backend
│   ├── .env          ← Your database credentials (edit this)
│   ├── schema.sql    ← Run this in pgAdmin to create all tables
│   ├── create_user.py← Run this once to create your login
│   ├── requirements.txt
│   └── ...
└── frontend/
    └── index.html    ← Open this in your browser (no build needed)
```

---

## Step 1 — Edit your .env

Open `backend/.env` and update your PostgreSQL credentials:

```
DATABASE_URL=postgresql://YOUR_USERNAME:YOUR_PASSWORD@localhost:5432/fleetflow
```

Your current .env uses:
- Username: postgres
- Password: root
- Database: fleetflow

Change if needed.

---

## Step 2 — Create the database

Open pgAdmin, right-click → Create → Database → name it `fleetflow`

---

## Step 3 — Run the SQL schema

In pgAdmin: open the `fleetflow` database → Query Tool → paste the contents of `backend/schema.sql` → Run (F5)

This creates all tables, indexes, and triggers.

---

## Step 4 — Install Python dependencies

Open a terminal in the `backend/` folder:

```bash
pip install -r requirements.txt
```

---

## Step 5 — Create your admin user

```bash
cd backend
python create_user.py
```

This creates:
- **Email:** admin@fleetflow.com
- **Password:** admin1234

---

## Step 6 — Start the backend

```bash
cd backend
python -m uvicorn main:app --reload
```

You should see:
```
FleetFlow is ready!
Uvicorn running on http://127.0.0.1:8000
```

---

## Step 7 — Open the frontend

Open `frontend/index.html` directly in your browser.

Log in with:
- **Email:** admin@fleetflow.com
- **Password:** admin1234

---

## Verify everything works

- Backend API docs: http://127.0.0.1:8000/docs
- DB test: http://127.0.0.1:8000/db-test
- Health: http://127.0.0.1:8000/health

---

## Deploying to Railway (optional)

1. Push `backend/` folder to GitHub
2. Go to railway.app → New Project → Deploy from GitHub
3. Add PostgreSQL service
4. Copy DATABASE_URL from Railway to environment variables
5. Add: SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
6. Railway reads `railway.toml` automatically — done!
7. Update `API_BASE` in `frontend/index.html` to your Railway URL
