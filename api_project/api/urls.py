from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token  # Import token view
from .views import BookList, BookViewSet

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book')

urlpatterns = [
    # Authentication endpoints
    path('auth-token/', obtain_auth_token, name='api_token_auth'),  # Token obtain endpoint
    
    # API endpoints
    path('books/', BookList.as_view(), name='book-list'),
    path('', include(router.urls)),
]