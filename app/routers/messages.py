from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List
from .. import models, schema, oauth2
from ..db import get_db
from ..redis_client import get_redis
import json

router = APIRouter(prefix="/messages", tags=["messages"])

# Store active WebSocket connections
active_connections: dict[int, WebSocket] = {}

@router.post("/", response_model=schema.MessageResponse, status_code=status.HTTP_201_CREATED)
async def send_message(
    message: schema.MessageCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    # Check if receiver exists
    receiver = db.query(models.User).filter(models.User.id == message.receiver_id).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create message
    new_message = models.Message(
        sender_id=current_user.id,
        receiver_id=message.receiver_id,
        content=message.content
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    
    # Cache in Redis (optional)
    try:
        redis = get_redis()
        cache_key = f"chat:{min(current_user.id, message.receiver_id)}:{max(current_user.id, message.receiver_id)}"
        redis.lpush(cache_key, json.dumps({
            "id": new_message.id,
            "sender_id": new_message.sender_id,
            "receiver_id": new_message.receiver_id,
            "content": new_message.content,
            "created_at": str(new_message.created_at)
        }))
        redis.ltrim(cache_key, 0, 99)  # Keep last 100 messages
    except:
        pass  # Redis not available, skip caching
    
    # Send via WebSocket if receiver is online
    if message.receiver_id in active_connections:
        await active_connections[message.receiver_id].send_json({
            "type": "new_message",
            "message": {
                "id": new_message.id,
                "sender_id": current_user.id,
                "sender_name": current_user.name,
                "content": new_message.content,
                "created_at": str(new_message.created_at)
            }
        })
    
    return new_message

@router.get("/", response_model=List[schema.MessageResponse])
async def get_messages(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    # Try Redis cache first (if available)
    try:
        redis = get_redis()
        cache_key = f"chat:{min(current_user.id, user_id)}:{max(current_user.id, user_id)}"
        cached = redis.lrange(cache_key, 0, -1)
        if cached:
            return [json.loads(msg) for msg in reversed(cached)]
    except:
        pass  # Redis not available, use database
    
    # Use database
    messages = db.query(models.Message).filter(
        ((models.Message.sender_id == current_user.id) & (models.Message.receiver_id == user_id)) |
        ((models.Message.sender_id == user_id) & (models.Message.receiver_id == current_user.id))
    ).order_by(models.Message.created_at.desc()).limit(100).all()
    
    return list(reversed(messages))

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    active_connections[user_id] = websocket
    
    try:
        while True:
            data = await websocket.receive_text()
            # Keep connection alive
    except WebSocketDisconnect:
        del active_connections[user_id]
