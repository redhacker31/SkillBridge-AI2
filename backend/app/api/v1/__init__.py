"""
SkillBridge AI — API v1.

Version 1 of the SkillBridge AI API.
All v1 endpoints are registered on this router.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/ping", tags=["system"])
async def ping() -> dict[str, str]:
    """Simple ping endpoint for API v1 availability checks."""
    return {"message": "pong", "api_version": "v1"}
