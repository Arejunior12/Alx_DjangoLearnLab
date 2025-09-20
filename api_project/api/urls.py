from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet

# Create a router and register our ViewSet
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book')

urlpatterns = [
    # Route for the original BookList view (ListAPIView) - kept for compatibility
    path('books/', BookList.as_view(), name='book-list'),
    
    # Include all router-generated URLs for the ViewSet
    path('', include(router.urls)),
]