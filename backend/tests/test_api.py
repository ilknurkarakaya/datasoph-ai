"""
Essential API tests for DataSoph AI
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test basic health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()

def test_root_endpoint():
    """Test root endpoint returns service info"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "DataSoph AI" in data["message"]

def test_ai_capabilities():
    """Test AI capabilities endpoint"""
    response = client.get("/api/v1/ai/capabilities")
    assert response.status_code == 200
    data = response.json()
    assert "intelligent_ai" in data
    assert "analytics_capabilities" in data

def test_services_status():
    """Test services status endpoint"""
    response = client.get("/api/v1/services/status")
    assert response.status_code == 200
    data = response.json()
    assert "services" in data
    assert "offline_mode" in data

@pytest.mark.asyncio
async def test_file_upload():
    """Test file upload functionality"""
    test_content = b"test,data\n1,2\n3,4"
    files = {"file": ("test.csv", test_content, "text/csv")}
    
    response = client.post("/api/v1/upload", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "file_id" in data 