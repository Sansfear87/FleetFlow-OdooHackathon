import os, logging, time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from database import verify_database_connection
from api.v1.router import api_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting FleetFlow...")
    verify_database_connection()
    logger.info("FleetFlow is ready!")
    yield

app = FastAPI(title="FleetFlow API", version="1.0.0", lifespan=lifespan)

app.add_middleware(CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    logger.info(f"{request.method} {request.url.path} | {response.status_code} | {(time.time()-start)*1000:.0f}ms")
    return response

app.include_router(api_router, prefix="/api/v1")

@app.get("/", tags=["System"])
def root(): return {"message": "FleetFlow API running. Docs at /docs"}

@app.get("/health", tags=["System"])
def health(): return {"status": "healthy", "environment": os.getenv("ENVIRONMENT","development")}
