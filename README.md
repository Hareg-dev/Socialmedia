# 🌐 Social Media Backend (FastAPI)

A backend learning project for building a fully functional **Social Media API** using **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **JWT authentication**.

This project helps you understand how modern social media platforms handle:
- User authentication
- Posts & comments
- Database migrations
- API structuring and routing
- Security (JWT, hashing)
- Backend architecture

---

##  Features

###  User System
- User registration
- User login
- Password hashing
- JWT access token generation

###  Posts
- Create posts  
- Get all posts  
- Get posts per user  

###  Comments
- Add comments to posts
- Fetch comments for posts

### 🔐 Security
- JWT authentication
- Protected routes
- Password hashing with bcrypt

---

##  Tech Stack

| Technology       | Purpose |
|------------------|---------|
| **FastAPI**      | Web framework |
| **PostgreSQL**   | Database |
| **SQLAlchemy**   | ORM |
| **Alembic**      | Migrations |
| **Pydantic**     | Schemas & validation |
| **Uvicorn**      | ASGI server |

---

##  Project Structure

Socialmedia/
├── app/
│ ├── main.py
│ ├── schema.py
│ ├── models.py
│ ├── routers/
│ ├── utils/
│ └── database.py
├── alembic/
├── requirements.txt
├── pyproject.toml
├── uv.lock
├── bruno-tests/
├── .env
└── README.md


---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Hareg-dev/Socialmedia.git
cd Socialmedia

