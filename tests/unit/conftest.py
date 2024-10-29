import pytest
from fastapi.testclient import TestClient
from src.main.app import app
import uuid

def build_user():
        return {
            "id": str(uuid.uuid4()), 
            "first_name": "Tyler",
            "middle_name": "Austin",
            "last_name": "Powell",
            "email_address": "test@me.com",
            "phone_number": "123-456-7890"
        }

@pytest.fixture
def client():
    with TestClient(app) as client:
        users = {}
        for _ in range(10):
            user = build_user()
            users[user['id']] = user
        app.state.user_repo.users = users
        yield client