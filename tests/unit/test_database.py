import uuid
import pytest 
from src.main.database import UserRepository


class TestUserRepository():

    @pytest.fixture
    def user_repository(self):
        yield UserRepository()

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
        assert user_repository.users == {user["id"]: user}

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
        assert sample_user['id'] not in user_repository.users
        assert sample_user == deleted_user
        