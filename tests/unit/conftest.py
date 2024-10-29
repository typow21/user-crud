import pytest
from fastapi.testclient import TestClient
from src.main.app import app

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client