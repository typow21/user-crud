from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"Hello": "World"}

@app.get("/users")
def get_users():
    return [{"Hello": "World"}, {"Hello": "World"}]


