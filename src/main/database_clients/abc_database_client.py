from abc import ABC, abstractmethod

class AbcDatabaseClient(ABC):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AbcDatabaseClient, cls).__new__(cls)
        return cls._instance

    @abstractmethod
    def get_data(self, key: str) -> dict:
        pass
    
    @abstractmethod
    def get_all_data(self) -> list[dict]:
        pass

    @abstractmethod
    def add_data(self, key, data) -> dict:
        pass

    @abstractmethod
    def delete_data(self, key) -> dict:
        pass

