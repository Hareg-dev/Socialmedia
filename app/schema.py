from pydantic import EmailStr, BaseModel, conint
from typing import Optional
from datetime import datetime


# User schemas
class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int

    model_config = {
        "from_attributes": True  
    }

# Post schemas
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    media_url: Optional[str] = None
    media_type: Optional[str] = None

class PostCreate(PostBase):
    pass

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    media_url: Optional[str] = None
    media_type: Optional[str] = None
    author: UserResponse
    created_at: Optional[datetime] = None
    
    model_config = {
        "from_attributes": True 
    }

class PostWithVotes(BaseModel):
    Post: PostResponse
    votes: int
    
    model_config = {
        "from_attributes": True 
    }

# Comment schemas
class CommentCreate(BaseModel):
    post_id: Optional[int] = None
    content: str

class CommentResponse(BaseModel):
    id: int
    user_id: int
    post_id: int
    content: str
    created_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True 
    }

# Auth schemas
class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

