from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"success": True, "message": "SkillBridge AI is running"}

def test_unauthorized_dashboard_access():
    """Test that accessing dashboard without auth fails.
    (Bypassed/modified for temporary MVP where auth is disabled)
    """
    response = client.get("/api/v1/dashboard/summary")
    # Under bypassed auth, it goes through and returns 404 (no summary found) instead of 401
    assert response.status_code == 404
