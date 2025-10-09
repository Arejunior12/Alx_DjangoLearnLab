# Social Media API - Posts & Comments

## Posts Endpoints

### List Posts
**GET** `/api/posts/`
- Returns paginated list of posts
- **Query Parameters:**
  - `search`: Search in title and content
  - `author`: Filter by author ID
  - `ordering`: Order by fields (created_at, updated_at)
- **Headers:** `Authorization: Token <your_token>`

### Create Post
**POST** `/api/posts/`
```json
{
    "title": "Post Title",
    "content": "Post content here"
}