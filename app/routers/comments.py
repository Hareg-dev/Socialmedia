from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List
from .. import models, schema
from ..db import engine, SessionLocal, Base, get_db
from .. import oauth2

router= APIRouter(
    prefix= "/comments",
    tags= ["comments"]
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schema.CommentResponse])
async def get_comments( db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    comments = db.query(models.Comment).all()
    return comments

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schema.CommentResponse)
async def get_comment(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    comment = db.query(models.Comment).filter(models.Comment.id == id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return comment

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    try:
        comment = db.query(models.Comment).filter(models.Comment.id == id).first()
        if not comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
        if comment.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this comment")  
        db.delete(comment)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.CommentResponse)
async def create_comment(comment: schema.CommentCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # If no post_id provided, use the latest post
    if comment.post_id is None:
        latest_post = db.query(models.Post).order_by(models.Post.id.desc()).first()
        if not latest_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts available to comment on")
        post_id = latest_post.id
    else:
        post = db.query(models.Post).filter(models.Post.id == comment.post_id).first()
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {comment.post_id} not found")
        post_id = comment.post_id
    
    new_comment = models.Comment(user_id=current_user.id, post_id=post_id, content=comment.content)    
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment
        
@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schema.CommentResponse)
async def update_comment(id: int, updated_comment: schema.CommentCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    try:
        comment = db.query(models.Comment).filter(models.Comment.id == id).first()
        if not comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
        if comment.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this comment")  
        
        comment.user_id = updated_comment.user_id
        comment.post_id = updated_comment.post_id
        comment.content = updated_comment.content
        
        db.commit()
        db.refresh(comment)
        return comment
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

