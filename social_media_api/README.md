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