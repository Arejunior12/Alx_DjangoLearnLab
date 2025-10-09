# Social Media API - Follow & Feed Features

## Follow Management Endpoints

### Follow a User
**POST** `/api/auth/follow/{user_id}/`
- Follow another user
- **Headers:** `Authorization: Token <your_token>`
- **Response:**
```json
{
    "message": "You are now following username",
    "following": true,
    "followers_count": 5,
    "following_count": 3
}

# Social Media API - Notifications & Likes

## Likes Endpoints

### Like a Post
**POST** `/api/posts/{post_id}/like/`
- Like a specific post
- **Headers:** `Authorization: Token <your_token>`
- **Response:**
```json
{
    "id": 1,
    "user": 1,
    "user_details": {
        "id": 1,
        "username": "user1"
    },
    "post": 1,
    "created_at": "2023-10-01T12:00:00Z"
}