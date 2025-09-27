from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    BookListView, 
    BookDetailView, 
    BookCreateView, 
    BookUpdateView, 
    BookDeleteView,
    BookListCreateView,
    BookRetrieveUpdateDestroyView
)

urlpatterns = [
    # Authentication endpoint
    path('auth-token/', obtain_auth_token, name='api_token_auth'),
    
    # Individual View URLs (Explicit approach - matches the task requirements)
    path('books/', BookListView.as_view(), name='book-list'),           # GET all books
    path('books/create/', BookCreateView.as_view(), name='book-create'), # POST create book
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'), # GET single book
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'), # PUT/PATCH update book
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'), # DELETE book
    
    # Alternative RESTful endpoints (bonus - more conventional API design)
    path('api/books/', BookListCreateView.as_view(), name='book-list-create'),
    path('api/books/<int:pk>/', BookRetrieveUpdateDestroyView.as_view(), name='book-retrieve-update-destroy'),
]