import os
import json
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from abc import ABC
from src.main.database_clients.abc_database_client import AbcDatabaseClient

Base = declarative_base()

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    data = Column(String)

class SqlDbClient(AbcDatabaseClient):
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            DATABASE_URL = os.getenv("POSTGRES_URL", "")

            # SQLAlchemy setup
            engine = create_engine(DATABASE_URL)
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            Base.metadata.create_all(bind=engine)
            self.initialized: bool = True
            self.database = SessionLocal()

    def get_data(self, key: str):
        with self.database as session:
            record = session.query(UserModel).filter(UserModel.key == key).first()
            return json.loads(record.data) if record else None

    def get_all_data(self):
        with self.database as session:
            records = session.query(UserModel).all()
            return [json.loads(record.data) for record in records]

    def add_data(self, key, data):
        with self.database as session:
            record = UserModel(key=key, data=json.dumps(data))
            session.add(record)
            session.commit()

    def delete_data(self, key):
        with self.database as session:
            record = session.query(UserModel).filter(UserModel.key == key).first()
            if record:
                data = json.loads(record.data)
                session.delete(record)
                session.commit()
                return data