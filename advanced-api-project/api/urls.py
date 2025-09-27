from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import BookListCreateView, BookRetrieveUpdateDestroyView

urlpatterns = [
    # Authentication
    path('auth-token/', obtain_auth_token, name='api_token_auth'),
    
    # Exact endpoints as requested
    path('books/', BookListCreateView.as_view(), name='book-list'),
    path('books/create/', BookListCreateView.as_view(), name='book-create'),  # POST to this URL
    path('books/<int:pk>/', BookRetrieveUpdateDestroyView.as_view(), name='book-detail'),
    path('books/<int:pk>/update/', BookRetrieveUpdateDestroyView.as_view(), name='book-update'),  # PUT/PATCH
    path('books/<int:pk>/delete/', BookRetrieveUpdateDestroyView.as_view(), name='book-delete'),  # DELETE
]