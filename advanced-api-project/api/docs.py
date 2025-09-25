"""
API Documentation for Advanced Book API

View Configurations and Custom Behavior:

1. BookListView (GET /api/books/)
   - Purpose: Retrieve paginated list of all books
   - Features: Search, filtering, ordering
   - Permissions: AllowAny (public read access)
   - Custom Hooks: Custom filter class for advanced filtering

2. BookCreateView (POST /api/books/create/)
   - Purpose: Create new book instances
   - Features: Custom validation, audit logging
   - Permissions: IsAuthenticated + IsAdminOrReadOnly
   - Custom Hooks: perform_create for business logic

3. BookUpdateView (PUT/PATCH /api/books/<id>/update/)
   - Purpose: Update existing book instances
   - Features: Partial update support, audit trail
   - Permissions: IsAuthenticated + IsAdminOrReadOnly
   - Custom Hooks: perform_update for change tracking

URL Patterns:
- List views use plural endpoints (/books/, /authors/)
- Detail views use singular with PK (/books/1/)
- Action-specific endpoints for clarity (/books/create/, /books/1/update/)

Custom Settings:
- Django Filter Backend: Enables field-based filtering
- SearchFilter: Provides search across multiple fields
- OrderingFilter: Allows result sorting by specified fields
- Custom Permission Classes: Role-based access control
"""

API_ENDPOINTS = {
    'books': {
        'list': '/api/books/',
        'create': '/api/books/create/',
        'detail': '/api/books/{id}/',
        'update': '/api/books/{id}/update/',
        'delete': '/api/books/{id}/delete/',
    },
    'authors': {
        'list': '/api/authors/',
        'create': '/api/authors/create/',
        'detail': '/api/authors/{id}/',
        'update': '/api/authors/{id}/update/',
        'delete': '/api/authors/{id}/delete/',
    }
}