from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    BookListCreateView,
    BookRetrieveUpdateDestroyView
)

urlpatterns = [
    # Authentication endpoint
    path('auth-token/', obtain_auth_token, name='api_token_auth'),
    
    # RESTful URL structure (recommended)
    path('books/', BookListCreateView.as_view(), name='book-list-create'),          # GET list, POST create
    path('books/<int:pk>/', BookRetrieveUpdateDestroyView.as_view(), name='book-detail'), # GET, PUT, PATCH, DELETE
]