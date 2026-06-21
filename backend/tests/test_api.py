from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"success": True, "message": "SkillBridge AI is running"}

def test_unauthorized_dashboard_access():
    """Test that accessing dashboard without auth fails."""
    response = client.get("/api/v1/dashboard/summary")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
