import uuid
import pytest 
from src.main.user_repository import UserRepository
from src.main.database_clients.abc_database_client import AbcDatabaseClient

class MockDatabaseClient(AbcDatabaseClient):
    def __init__(self):
        self._storage = {}

    def get_data(self, key: str) -> dict:
        return self._storage.get(key, None)

    def get_all_data(self) -> list[dict]:
        return [data for data in self._storage.values()]

    def add_data(self, key: str, data: dict) -> None:
        self._storage[key] = data

    def delete_data(self, key: str) -> None:
        if key in self._storage:
            data = self._storage.get(key)
            del self._storage[key]
            return data
    
    def cleanup(self):
        self._instance = None
        self._storage.clear()

class TestUserRepository():

    @pytest.fixture
    def user_repository(self):
        user_repo = UserRepository(db_client = MockDatabaseClient())
        yield user_repo
        user_repo.cleanup()
        

    def build_user(self):
        return {
            "id": str(uuid.uuid4()), 
            "first_name": "Tyler",
            "middle_name": "Austin",
            "last_name": "Powell",
            "email_address": "test@me.com",
            "phone_number": "123-456-7890"
        }

    def test_add_user(self, user_repository):
        user = {
            "id": str(uuid.uuid4()), 
            "first_name": "Tyler",
            "middle_name": "Austin",
            "last_name": "Powell",
            "email_address": "test@me.com",
            "phone_number": "123-456-7890"
        }
        actual = user_repository.add_user(user)
        assert user == actual
        assert user_repository.db_client._storage == {user["id"]: user}

    def test_get_all_users(self, user_repository):
        users = [user_repository.add_user(self.build_user()) for _ in range(10)]
        actual = user_repository.get_all_users()
        assert actual == users

    def test_get_user(self, user_repository):
        user = self.build_user()
        user_repository.add_user(user)
        actual = user_repository.get_user(user['id'])
        assert actual == user

    def test_delete_user(self, user_repository):
        users = [user_repository.add_user(self.build_user()) for _ in range(10)]
        sample_user = users[0]
        deleted_user = user_repository.delete_user(sample_user['id'])
        assert len(users) == 10
        assert sample_user['id'] not in user_repository.db_client._storage
        assert sample_user == deleted_user
        