"""
SkillBridge AI — Main API Router.

Aggregates all versioned API sub-routers into a single
router mounted at the application level.
"""

from fastapi import APIRouter

from app.api.v1 import router as v1_router

api_router = APIRouter()

# Mount v1 API
api_router.include_router(v1_router, prefix="/v1", tags=["v1"])
