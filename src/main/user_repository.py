from src.main.user_model import User
from pydantic import ValidationError 
from typing import Union
import json
import os
from src.main.database_clients.abc_database_client import AbcDatabaseClient

class UserRepository:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(UserRepository, cls).__new__(cls)
        return cls._instance

    def __init__(self, db_client: AbcDatabaseClient = None):
        if not hasattr(self, 'initialized'):
            self.initialized: bool = True
            if not db_client:
                raise TypeError("Missing required parameter on initialization: 'db_client'")
            if not isinstance(db_client, AbcDatabaseClient):
                raise TypeError("db_client must be instance of AbcDatabaseClient")
            self.db_client = db_client

    def add_user(self, user: dict) -> Union[dict, None]:
        if not isinstance(user, dict):
            raise TypeError("user param must be type dict.")
        try:
            validated_user = User(**user).model_dump()
        except ValidationError as e:
            return None
        self.db_client.add_data(validated_user['id'], validated_user)
        return validated_user

    def get_all_users(self) -> list[dict]:
        return self.db_client.get_all_data()

    def get_user(self, id: str) -> Union[dict, None]:
        if not isinstance(id, str):
            raise TypeError("id param must be type str.")

        # Retrieve user from Redis by id
        user_data = self.db_client.get_data(id)
        return user_data if user_data else None
    
    def delete_user(self, id: str)  -> Union[dict, None]:
        if not isinstance(id, str):
            raise TypeError("id param must be type str.")
        return self.db_client.delete_data(id)

    def cleanup(self):
        self.db_client.cleanup()
        UserRepository._instance = None
