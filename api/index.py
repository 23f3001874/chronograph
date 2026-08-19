"""Vercel Serverless Entry Point for ChronoGraph FastAPI Backend."""

import os
import sys
from pathlib import Path

# Add backend directory to Python path for serverless imports
root_dir = Path(__file__).resolve().parent.parent
backend_dir = root_dir / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# Import FastAPI app from backend
from app.main import app

# Export ASGI app for Vercel
__all__ = ["app"]
