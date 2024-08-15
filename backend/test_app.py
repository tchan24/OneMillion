import pytest
from app import app

@pytest.fixture
def client():
    return app.test_client()

def test_login(client):
    response = client.post('/api/login', json={'username': 'testuser', 'password': 'testpass'})
    assert response.status_code == 200

def test_create_project(client):
    response = client.post('/api/projects', json={'name': 'Test Project', 'description': 'A test project'})
    assert response.status_code == 201