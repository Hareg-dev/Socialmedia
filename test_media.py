import requests

BASE_URL = "http://127.0.0.1:8000"

# 1. Login to get token
login_data = {
    "email": "your_email@example.com",
    "password": "your_password"
}
response = requests.post(f"{BASE_URL}/login", json=login_data)
token = response.json()["access_token"]

headers = {"Authorization": f"Bearer {token}"}

# 2. Upload image
with open("test_image.jpg", "rb") as f:
    files = {"file": ("test_image.jpg", f, "image/jpeg")}
    response = requests.post(f"{BASE_URL}/posts/upload", files=files, headers=headers)
    print("Upload response:", response.json())
    media_data = response.json()

# 3. Create post with media
post_data = {
    "title": "Test Post with Image",
    "content": "This is a test post with an image",
    "published": True,
    "media_url": media_data["media_url"],
    "media_type": media_data["media_type"]
}
response = requests.post(f"{BASE_URL}/posts/", json=post_data, headers=headers)
print("Post created:", response.json())

# 4. Get posts
response = requests.get(f"{BASE_URL}/posts/", headers=headers)
print("Posts:", response.json())
