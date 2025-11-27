# 🌐 Social Media Backend (FastAPI)

A fully functional **Social Media API** using **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **JWT authentication**, and **WebSocket** for real-time chat.

This project demonstrates how modern social media platforms handle:
- User authentication & authorization
- Posts with media (images & videos)
- Comments & likes/votes
- Real-time messaging
- Database migrations
- API structuring and routing
- Security (JWT, password hashing)
- File uploads & static file serving

---

## ✨ Features

### 👤 User System
- User registration
- User login with JWT tokens
- Password hashing with bcrypt
- Profile management (update/delete)
- Protected routes

### 📝 Posts
- Create text posts
- Upload images (JPEG, PNG, GIF, WebP)
- Upload videos (MP4, MPEG, QuickTime)
- Edit/Delete own posts
- Search & pagination
- View posts with vote counts

### 💬 Comments
- Add comments to posts
- Edit/Delete own comments
- Fetch comments for posts

### 👍 Votes/Likes
- Like/Unlike posts
- Vote count per post
- Prevent duplicate votes

### 💬 Real-time Chat
- Send direct messages
- WebSocket real-time delivery
- Redis caching (optional)
- Chat history
- Online status detection
- Read receipts

---

## 🛠️ Tech Stack

| Technology       | Purpose |
|------------------|---------|
| **FastAPI**      | Web framework |
| **PostgreSQL**   | Database |
| **SQLAlchemy**   | ORM |
| **Alembic**      | Migrations |
| **Pydantic**     | Schemas & validation |
| **Uvicorn**      | ASGI server |
| **WebSockets**   | Real-time chat |
| **Redis**        | Caching (optional) |
| **Bcrypt**       | Password hashing |
| **JWT**          | Authentication |

---

## 📁 Project Structure

```
fastapi/
├── app/
│   ├── main.py              # Main application
│   ├── models.py            # Database models
│   ├── schema.py            # Pydantic schemas
│   ├── auth.py              # Login endpoint
│   ├── oauth2.py            # JWT authentication
│   ├── db.py                # Database connection
│   ├── config.py            # Settings
│   ├── utils.py             # Password hashing
│   ├── redis_client.py      # Redis connection
│   └── routers/
│       ├── users.py         # User endpoints
│       ├── posts.py         # Post endpoints
│       ├── comments.py      # Comment endpoints
│       ├── votes.py         # Vote endpoints
│       └── messages.py      # Chat endpoints
├── alembic/                 # Database migrations
├── uploads/                 # Uploaded media files
├── requirements.txt
├── chat_test.html          # Browser chat test
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Hareg-dev/Socialmedia.git
cd Socialmedia
```

### 2️⃣ Create virtual environment
```bash
uv venv
.venv\Scripts\activate  # Windows
```

### 3️⃣ Install dependencies
```bash
uv pip install -r requirements.txt
```

### 4️⃣ Setup PostgreSQL
- Install PostgreSQL
- Create database: `fastapi-cource`
- Update `.env` file with your credentials

### 5️⃣ Run migrations
```bash
alembic upgrade head
```

### 6️⃣ Start the server
```bash
fastapi dev app/main.py
```

Server runs at: `http://localhost:8000`
API Docs: `http://localhost:8000/docs`

---

## 🚀 API Endpoints

### Authentication
- `POST /users/` - Register new user
- `POST /login` - Login and get JWT token
- `GET /users/me` - Get current user

### Posts
- `POST /posts/upload` - Upload image/video
- `POST /posts/` - Create post
- `GET /posts/` - Get all posts
- `GET /posts/{id}` - Get single post
- `PUT /posts/{id}` - Update post
- `DELETE /posts/{id}` - Delete post

### Comments
- `POST /comments/` - Add comment
- `GET /comments/` - Get all comments
- `PUT /comments/{id}` - Update comment
- `DELETE /comments/{id}` - Delete comment

### Votes
- `POST /votes/` - Like/Unlike post

### Messages (Chat)
- `POST /messages/` - Send message
- `GET /messages/?user_id={id}` - Get chat history
- `WS /messages/ws/{user_id}` - WebSocket connection

---

## 🧪 Testing

### Using FastAPI Docs
1. Go to `http://localhost:8000/docs`
2. Click "Authorize" and enter JWT token
3. Test any endpoint

### Using Bruno
1. Create user: `POST /users/`
2. Login: `POST /login`
3. Copy token and add to headers: `Authorization: Bearer {token}`
4. Test endpoints

### Testing Chat (Browser)
1. Open `chat_test.html` in Chrome
2. Open `chat_test.html` in Edge
3. Login as different users
4. Start chatting in real-time!

---

## 📝 Environment Variables

Create `.env` file:
```env
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=your_password
DATABASE_NAME=fastapi-cource
HOST=localhost
PORT=5432
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 🎯 Similar to:
- **Facebook** - Posts, comments, likes, chat
- **Instagram** - Media posts, likes, comments
- **Twitter** - Posts, likes
- **WhatsApp** - Real-time messaging

---

## 🔜 Future Enhancements
- Celery background tasks
- User profile pictures
- Friend/Follow system
- News feed algorithm
- Push notifications
- Group chats
- Stories feature
- Video calls

---

## 📚 Documentation
- [Media Upload Guide](MEDIA_USAGE.md)
- [Chat System Guide](CHAT_USAGE.md)
- [Complete Features](FEATURES.md)

---

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first.

---

## 📄 License
MIT

---

**Built with ❤️ using FastAPI**
