import pytest
from src.main.app import app
from src.main.user_model import User
from unittest.mock import Mock, patch
import uuid
import json

class TestApp:

    def build_user(self):
        return {
            "id": str(uuid.uuid4()), 
            "first_name": "Tyler",
            "middle_name": "Austin",
            "last_name": "Powell",
            "email_address": "test@me.com",
            "phone_number": "123-456-7890"
        }

    @pytest.fixture(autouse=True)
    def setup_redis_mock(self):

        with patch('src.main.database_clients.redis_database_client.redis.Redis') as MockRedis:
            self.mock_redis = MockRedis.return_value
            self.mock_redis.keys = Mock(return_value=None)
            self.mock_redis.set = Mock(return_value=True)
            self.mock_redis.get = Mock(return_value=None)
            self.mock_redis.delete = Mock(return_value=1)
            yield

    @pytest.mark.asyncio
    async def test_app_start(self, client):
        url = "http://localhost:8000/"
        response = client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert data == {"Hello": "World"}
    
    @pytest.mark.asyncio
    async def test_app_get_users(self, client):

        user_data = self.build_user()
        self.mock_redis.get.return_value = json.dumps(user_data)
        self.mock_redis.keys.return_value = [user_data['id']]
        url = "http://localhost:8000/users"
        response = client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert data == [user_data]

    @pytest.mark.asyncio
    async def test_app_get_user(self, client):
        user = self.build_user()

        self.mock_redis.get.return_value = json.dumps(user)
        
        url = f"http://localhost:8000/user/{user.get('id')}"
        response = client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert data == user
        self.mock_redis.get.assert_called_once_with(user['id'])

    @pytest.mark.asyncio
    async def test_app_delete_user(self, client):
        user = self.build_user()
        self.mock_redis.delete.return_value = 1
        self.mock_redis.get.return_value = json.dumps(user)
        url = f"http://localhost:8000/user/{user.get('id')}"
        response = client.delete(url)
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == user['id']
        self.mock_redis.delete.assert_called_once_with(user['id'])

    @pytest.mark.asyncio
    async def test_app_post_user(self, client):
        user_to_add = self.build_user()

        self.mock_redis.set.return_value = True
        
        url = "http://localhost:8000/user"
        response = client.post(url=url, json=user_to_add)
        assert response.status_code == 200
        data = response.json()
        self.mock_redis.set.assert_called_once_with(data['id'], json.dumps(data))
