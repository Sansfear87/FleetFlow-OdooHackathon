# api/v1/router.py

from fastapi import APIRouter

from api.v1 import auth, users, vehicles, drivers, trips, maintenance, fuel, expenses

api_router = APIRouter()

# Auth must be first — no token required for /auth/token
api_router.include_router(auth.router)

api_router.include_router(users.router)
api_router.include_router(vehicles.router)
api_router.include_router(drivers.router)
api_router.include_router(trips.router)
api_router.include_router(maintenance.router)
api_router.include_router(fuel.router)
api_router.include_router(expenses.router)
