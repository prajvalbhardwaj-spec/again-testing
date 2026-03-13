from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.database import engine, SessionLocal
from app.models import Base
from app.seed_logic import seed_database
from app.routers import auth, users, blogs


# ── Lifespan: create tables + seed on first run ───────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    print("Tables created")

    db = SessionLocal()
    try:
        message = seed_database(db)
        print(message)
    finally:
        db.close()

    yield


app = FastAPI(title="Blog API", version="1.0.0", lifespan=lifespan)

# ── CORS ──────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Global error handler ──────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
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
            return {"message": "Already seeded, skipping"}
        return {"message": "Database seeded!"}
    finally:
        db.close()
