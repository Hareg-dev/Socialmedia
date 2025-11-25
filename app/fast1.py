from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional as OPTIONAL


app = FastAPI()

my_posts = [
    {
    "title": "my first post",
    "content": "this is my first post content",
    "id": 1
   },
   {
    "title": "art of war",
    "content": "this is my first book content",
    "id": 2
    },
    {
    "title": "my third post",
    "content": "this is my third post content",
    "id": 3
    }
]

@app.post("/posts")
async def read_root():
    return {"message": my_posts}


@app.get("/")
async def read_root():
    return {"message": "Hello, Abel"}

@app.get("/home")
async def read_root():
    return {"message": "Hello, Welcome to home page"}

@app.get("/land")
async def read_root():
    return {"message": "Hello, welcome to landing page"}

@app.get("/child")
async def read_root():
    return {"message": "Hello, welcome to child page"}

@app.post("/post")
async def post(playload: dict = Body(...)):
    return {"message": f"namee is {playload['name']}, bussiness is {playload['startup']}"}

class Post(BaseModel):
    name: str
    startup: str
    funding: int
    partners: OPTIONAL[int] = None
    ipo: bool = False

@app.post("/comment")
async def comment(post: Post):
    #print(Post.name)
    print(post.dict())
    return {"message": f"title is {post.name}, content is {post.dict()}"}



@app.post("/greet")
async def greet_user():
    return {
        "message": f"Hello, man!",
        "age_next_year": 45
    }

@app.post("/data")
async def process_data():
    return {
        "original_value": "data.value",
        "processed_value": "processed_value"
    }


