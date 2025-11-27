from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, UploadFile, File
from sqlalchemy.orm import Session
from .. import oauth2
from .. import models, schema
from typing import Optional, List
from ..db import engine, SessionLocal, Base, get_db
from sqlalchemy import func
import os
import shutil
import time
from pathlib import Path

router= APIRouter(
    prefix= "/posts"
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
ALLOWED_VIDEO_TYPES = {"video/mp4", "video/mpeg", "video/quicktime"}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_media(
    file: UploadFile = File(...),
    current_user: int = Depends(oauth2.get_current_user)
):
    if file.content_type not in ALLOWED_IMAGE_TYPES and file.content_type not in ALLOWED_VIDEO_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type. Only images and videos allowed")
    
    file_ext = file.filename.split(".")[-1]
    file_name = f"{current_user.id}_{int(time.time() * 1000)}.{file_ext}"
    file_path = UPLOAD_DIR / file_name
    
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    media_type = "image" if file.content_type in ALLOWED_IMAGE_TYPES else "video"
    return {"media_url": f"/uploads/{file_name}", "media_type": media_type}

@router.post("/", response_model=schema.PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(post: schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(author_id=current_user.id, **post.dict())   
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/", response_model=List[schema.PostWithVotes], status_code=status.HTTP_200_OK)
async def get_posts(
    db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user), 
    limit: int = 10, skip: int = 0, 
    search: Optional[str] = ""
    ):
    posts = (
        db.query(models.Post, func.count(models.Votes.post_id).label("votes"))
        .join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.author_id == current_user.id, models.Post.title.contains(search))
        .limit(limit).offset(skip)
        .all()
    )
    return posts

@router.get("/{id}", response_model=schema.PostResponse, status_code=status.HTTP_200_OK)
async def get_post(
    id: int, db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user)
    ):
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    post = (
        db.query(models.Post, func.count(models.Votes.post_id).label("votes"))
        .join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.author_id == current_user.id, models.Post.title.contains(search))
        .limit(limit).offset(skip)  
        .filter(models.Post.id == id).first()
    )

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    try:
        post = db.query(models.Post).filter(models.Post.id == id).first()
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        if post.author_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post") 
        db.delete(post)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.put("/{id}", response_model=schema.PostResponse, status_code=status.HTTP_200_OK)
async def update_post(id: int, post_update: schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    try:
        post = db.query(models.Post).filter(models.Post.id == id).first()
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        if post.author_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this post")     
        post.title = post_update.title
        post.content = post_update.content
        post.published = post_update.published
        db.commit()
        db.refresh(post)
        return post
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))