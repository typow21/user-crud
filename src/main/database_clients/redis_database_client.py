import os
import json
import redis
from abc import ABC, abstractmethod
from src.main.database_clients.abc_database_client import AbcDatabaseClient

class RedisDbClient(AbcDatabaseClient):

    def __init__(self):
        self.redis_client = redis.Redis(
                    host=os.getenv('REDIS_HOST', 'localhost'), 
                    port=os.getenv('REDIS_PORT', 6379), 
                    db=0
                )

    def get_data(self, key: str):
        data = self.redis_client.get(key)
        return json.loads(data)
    
    def get_all_data(self):
        keys = self.redis_client.keys()
        all_data = []
        
        for key in keys:
            data = self.redis_client.get(key)
            if data:
                all_data.append(json.loads(data))
        return all_data

    def add_data(self, key, data):
        return self.redis_client.set(key, json.dumps(data))

    def delete_data(self, key):
        data = json.loads(self.redis_client.get(key))
        if data:
            self.redis_client.delete(key)
            return data

    def close_connection(self):
        self.redis_client.close()
