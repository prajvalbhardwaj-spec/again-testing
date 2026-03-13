import logging
import traceback
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.logging_config import setup_logging
from app.middleware import RequestLoggingMiddleware
from app.database import engine, SessionLocal
from app.models import Base
from app.seed_logic import seed_database
from app.routers import auth, users, blogs

setup_logging()
logger = logging.getLogger("app.main")


# ── Lifespan: create tables + seed on first run ───────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Tables created")
    except Exception as e:
        logger.error("Failed to create tables: %s", e, exc_info=True)
        raise

    db = SessionLocal()
    try:
        message = seed_database(db)
        logger.info(message)
    except Exception as e:
        logger.error("Database seeding failed: %s", e, exc_info=True)
    finally:
        db.close()

    logger.info("App started")
    yield


app = FastAPI(title="Blog API", version="1.0.0", lifespan=lifespan)

# ── Middleware (order matters: logging wraps everything) ───────
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── HTTP exception handler (404, 400, 403, etc.) ──────────────
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 404:
        logger.warning("404 Not Found: %s %s", request.method, request.url.path)
    elif exc.status_code >= 500:
        logger.error(
            "HTTP %s on %s %s: %s",
            exc.status_code, request.method, request.url.path, exc.detail
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


# ── Global unhandled exception handler ───────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.critical(
        "UNHANDLED EXCEPTION on %s %s\n%s",
        request.method,
        request.url.path,
        traceback.format_exc(),
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


# ── Routers ───────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(blogs.router)


# ── Root ──────────────────────────────────────────────────────
@app.get("/")
def root():
    return {"message": "API is running"}


# ── Manual seed endpoint ──────────────────────────────────────
@app.post("/seed")
def manual_seed():
    db = SessionLocal()
    try:
        message = seed_database(db)
        if "skipping" in message:
            logger.info("POST /seed — already seeded, skipping")
            return {"message": "Already seeded, skipping"}
        logger.info("POST /seed — database seeded successfully")
        return {"message": "Database seeded!"}
    finally:
        db.close()
