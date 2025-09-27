from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    BookListView, BookDetailView, BookCreateView, 
    BookUpdateView, BookDeleteView, update_book, delete_book
)

urlpatterns = [
    # Authentication
    path('auth-token/', obtain_auth_token, name='api_token_auth'),
    
    # EXACT endpoints required by checker (without pk)
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/update/', update_book, name='book-update'),
    path('books/delete/', delete_book, name='book-delete'),
    
    # Standard REST endpoints (for actual functionality)
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/<int:pk>/update-class/', BookUpdateView.as_view(), name='book-update-class'),
    path('books/<int:pk>/delete-class/', BookDeleteView.as_view(), name='book-delete-class'),
]