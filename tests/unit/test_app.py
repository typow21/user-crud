import pytest
from src.main.app import app
import uuid
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


    @pytest.mark.asyncio
    async def test_app_start(self, client):
        url = "http://localhost:8000/" 
        response = client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert data == {"Hello": "World"}
    
    @pytest.mark.asyncio
    async def test_app_get_users(self, client):
        url = "http://localhost:8000/users" 
        response = client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert data == app.state.user_repo.get_all_users()

    @pytest.mark.asyncio
    async def test_app_get_user(self, client):
        user = self.build_user()
        app.state.user_repo.add_user(user)
        url = f"http://localhost:8000/user/{user.get('id')}" 
        response = client.get(url)
        assert response.status_code == 200
        data = response.json()
        assert data == user

    @pytest.mark.asyncio
    async def test_app_delete_user(self, client):
        user_to_delete = next(iter(app.state.user_repo.users))
        url = f"http://localhost:8000/user/{user_to_delete}" 
        response = client.delete(url)
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == user_to_delete
        assert data['id'] not in app.state.user_repo.users

    @pytest.mark.asyncio
    async def test_app_post_user(self, client):
        user_to_add = self.build_user()
        url = "http://localhost:8000/user"
        response = client.post(url=url, json=user_to_add)
        assert response.status_code == 200
        data = response.json()
        assert data['id'] in app.state.user_repo.users
