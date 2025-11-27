# Chat System Usage

## Setup Redis (Required)

**Windows:**
1. Download Redis from: https://github.com/microsoftarchive/redis/releases
2. Install and run: `redis-server`

Or use Docker:
```bash
docker run -d -p 6379:6379 redis
```

## API Endpoints

### Send Message
**POST** `/messages/`
```json
{
  "receiver_id": 2,
  "content": "Hello!"
}
```

### Get Chat History
**GET** `/messages/?user_id=2`

Returns last 100 messages (cached in Redis)

### WebSocket Connection (Real-time)
**WS** `/messages/ws/{your_user_id}`

Connect to receive real-time messages

## Testing in Bruno

1. **Send Message:**
   - POST `http://localhost:8000/messages/`
   - Headers: `Authorization: Bearer YOUR_TOKEN`
   - Body: `{"receiver_id": 2, "content": "Hi there!"}`

2. **Get Messages:**
   - GET `http://localhost:8000/messages/?user_id=2`
   - Headers: `Authorization: Bearer YOUR_TOKEN`

## Features

✅ Real-time messaging via WebSocket
✅ Redis caching (last 100 messages)
✅ Message history
✅ Online status detection
✅ Read receipts (is_read field)

## Frontend Example (JavaScript)

```javascript
// Connect to WebSocket
const ws = new WebSocket('ws://localhost:8000/messages/ws/1');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('New message:', data.message);
};

// Send message via API
fetch('/messages/', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    receiver_id: 2,
    content: 'Hello!'
  })
});
```
