from fastapi import FastAPI

from contextlib import asynccontextmanager
from src.main.user_repository import UserRepository
from src.main.user_model import UserRequest, User
from src.main.database_clients.redis_database_client import RedisDbClient
from src.main.database_clients.sql_database_client import SqlDbClient

@asynccontextmanager
async def lifespan(app: FastAPI):
    db_client = RedisDbClient()
    user_repo = UserRepository(db_client = db_client)
    app.state.user_repo = user_repo
    yield
    # Clean up the ML models and release the resources
    user_repo.cleanup()


app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"Hello": "World"}

@app.get("/users")
def get_users() -> list[User]:
    return UserRepository().get_all_users()

@app.get("/user/{id}")
def get_user_by_id(id: str)->User:
    return UserRepository().get_user(id)

@app.delete("/user/{id}")
def delete_user_by_id(id: str)->User:
    return UserRepository().delete_user(id)

@app.post("/user")
def post_user(user: UserRequest) -> User:
    #TODO make this more efficient, lots of dumping and validating
    user_dict = user.model_dump()
    return UserRepository().add_user(user_dict)
