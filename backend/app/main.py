"""Main FastAPI application entry point for ChronoGraph with lifespan persistence and production hardening."""

from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.dependencies import restore_from_snapshot, save_current_snapshot
from app.api.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI application lifespan handler for automatic startup restoration and shutdown persistence."""
    # Startup: Restore store from disk snapshot if present
    restore_from_snapshot()
    yield
    # Shutdown: Persist store snapshot atomically
    try:
        save_current_snapshot()
    except Exception:
        pass


app = FastAPI(
    title="ChronoGraph Reasoning API",
    description="Temporal Belief & Memory Reasoning Engine API powered by HydraDB Cloud",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Production-safe CORS configuration
allowed_origins_env = os.environ.get("ALLOWED_ORIGINS", "*")
allowed_origins = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
