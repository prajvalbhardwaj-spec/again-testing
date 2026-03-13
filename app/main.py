from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routers import auth, users, blogs

app = FastAPI(title="Blog API", version="1.0.0")

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
