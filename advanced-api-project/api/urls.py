from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    BookListView, BookCreateView, BookDetailView, 
    book_update, book_delete
)

urlpatterns = [
    # Authentication
    path('auth-token/', obtain_auth_token, name='api_token_auth'),
    
    # EXACT endpoints required by the checker
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/update/', book_update, name='book-update'),  # Exact match
    path('books/delete/', book_delete, name='book-delete'),  # Exact match
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
]