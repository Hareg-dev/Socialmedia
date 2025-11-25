from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schema
from .. import utils, oauth2
from ..db import get_db

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=schema.UserResponse)
async def get_current_user(
    current_user: models.User = Depends(oauth2.get_current_user)
):
    return current_user


@router.post("/", response_model=schema.UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    # Hash the provided password
    hashed_password = utils.hash(user.password)

    # Check if a user with the given email already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    # Create a new user instance with the hashed password
    db_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password
    )

    # Add the new user to the database, commit the transaction, and refresh the instance
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Return the newly created user
    return db_user

@router.get("/{user_id}", response_model=schema.UserResponse)
async def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Can only access your own profile")
    return current_user


@router.put("/{user_id}", response_model=schema.UserResponse)
async def update_user(
    user_id: str,
    user_update: schema.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Can only update your own profile")

    update_data = user_update.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["password"] = utils.hash(update_data["password"])

    user_query = db.query(models.User).filter(models.User.id == current_user.id)
    user_query.update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(current_user)
    return current_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Can only delete your own profile")

    user_query = db.query(models.User).filter(models.User.id == current_user.id)
    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
