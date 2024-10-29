from src.main.user_model import User
from pydantic import ValidationError 
from typing import Union

class UserRepository:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(UserRepository, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized: bool = True
            self.users: dict[str: dict] = {}

    def add_user(self, user: dict) -> Union[dict, None]:
        if not isinstance(user, dict):
            raise TypeError("user param must be type dict.")
        try:
            validated_user = User(**user).model_dump()
        except ValidationError as e:
            return None
        self.users[validated_user['id']] = validated_user
        return validated_user

    def get_all_users(self) -> list[dict]:
        return [user for user in self.users.values()]

    def get_user(self, id: str) -> Union[dict, None]:
        if not isinstance(id, str):
            raise TypeError("id param must be type str.")
        user = self.users.get(id)
        return user
    
    def delete_user(self, id: str)  -> Union[dict, None]:
        if not isinstance(id, str):
            raise TypeError("id param must be type str.")
        user = self.users.get(id)
        if user:
            self.users.pop(id, None)
        return user