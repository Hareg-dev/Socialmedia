from fastapi import FastAPI
from .db import engine, Base, create_database_if_not_exists
from .routers import posts, users, comments, votes
from . import auth


app = FastAPI()
@app.on_event("startup")
def create_tables():
    create_database_if_not_exists()

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get("/", status_code=202)
async def home():
    return {"message": "Hello from home"}

@app.get("/landing", status_code=202)
async def landing():
    return {"message": "Hello from landing page"}
