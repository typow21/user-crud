from fastapi import FastAPI, HTTPException
import logging
from contextlib import asynccontextmanager
from src.main.user_repository import UserRepository
from src.main.user_model import UserRequest, User
from src.main.database_clients.redis_database_client import RedisDbClient
from src.main.database_clients.sql_database_client import SqlDbClient
from prometheus_fastapi_instrumentator import Instrumentator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    db_client = RedisDbClient()
    user_repo = UserRepository(db_client = db_client)
    app.state.user_repo = user_repo
    
    yield

    user_repo.cleanup()


app = FastAPI(lifespan=lifespan)

Instrumentator().instrument(app).expose(app)

@app.get("/metrics") 
def metrics():
    return instrumentator.get_metrics()

@app.get("/")
def root():
    return {"Hello": "World"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/users")
def get_users() -> list[User]:
    return UserRepository().get_all_users()

@app.get("/user/{id}")
def get_user_by_id(id: str)->User:

    user = UserRepository().get_user(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/user/{id}")
def delete_user_by_id(id: str)->User:
    deleted_user = UserRepository().delete_user(id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")

    redis_client = RedisDbClient()
    redis_client.remove_from_set('email', deleted_user.get('email_address'))
    return deleted_user

def is_email_unique(email):
    redis_client = RedisDbClient()
    return not bool(redis_client.is_member_in_set('email', email))


@app.post("/user")
def post_user(user: UserRequest) -> User:
    # TODO make this more efficient, lots of dumping and validating
    user_dict = user.model_dump()
    if is_email_unique(user.email_address):
        added_user = UserRepository().add_user(user_dict)
        redis_client = RedisDbClient()
        redis_client.add_to_set("email", user.email_address)
        return added_user
    else:
        raise HTTPException(status_code=400, detail="Email already exists")
