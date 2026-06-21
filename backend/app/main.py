"""
SkillBridge AI — FastAPI Application Entry Point

Responsibilities:
- Initialize FastAPI app
- Configure CORS middleware
- Register API routers
- Initialize database on startup
"""

import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db
from app.routers import auth

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("skillbridge")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    # Startup
    logger.info("Starting SkillBridge AI...")
    init_db()
    logger.info("Database initialized.")

    # Create uploads directory if it doesn't exist
    uploads_path = Path(settings.upload_dir)
    uploads_path.mkdir(parents=True, exist_ok=True)
    logger.info("Upload directory ready: %s", uploads_path.resolve())

    logger.info("SkillBridge AI is ready!")
    yield
    # Shutdown
    logger.info("Shutting down SkillBridge AI...")


app = FastAPI(
    title="SkillBridge AI",
    description="AI-Powered Career Mentor & Resume Intelligence Platform",
    version="1.0.0",
    lifespan=lifespan,
)

# ──────────────────────────────────────────────
# CORS Middleware
# ──────────────────────────────────────────────
allow_origins = settings.cors_origin_list
allow_credentials = True
if "*" in allow_origins:
    allow_credentials = False

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ──────────────────────────────────────────────
# Routers Registration
# ──────────────────────────────────────────────
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
from app.routers import resume
app.include_router(resume.router, prefix="/api/v1/resume", tags=["Resume"])
from app.routers import dashboard
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])

# ──────────────────────────────────────────────
# Health Check
# ──────────────────────────────────────────────
@app.get("/api/v1/health", tags=["Health"])
def health_check():
    """Health check endpoint to verify the API is running."""
    return {
        "success": True,
        "message": "SkillBridge AI is running",
    }
