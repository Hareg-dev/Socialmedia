# Media Upload Usage

## Upload Image/Video

**Endpoint:** `POST /posts/upload`

**Headers:**
```
Authorization: Bearer <your_token>
Content-Type: multipart/form-data
```

**Body:** Form-data with file field


**Response:**
```json
{
  "media_url": "/uploads/1_1234567890.jpg",
  "media_type": "image"
}
```

## Create Post with Media

**Endpoint:** `POST /posts/`

**Body:**
```json
{
  "title": "My vacation photo",
  "content": "Beautiful sunset!",
  "published": true,
  "media_url": "/uploads/1_1234567890.jpg",
  "media_type": "image"
}
```

## Supported Formats

**Images:** JPEG, PNG, GIF, WebP
**Videos:** MP4, MPEG, QuickTime
**Max Size:** 50MB
