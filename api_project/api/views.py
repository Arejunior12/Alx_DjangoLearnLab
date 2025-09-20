from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer

# Keep your existing ListAPIView for backward compatibility
class BookList(generics.ListAPIView):
    """API view to list all books"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# Add the ViewSet for full CRUD operations
class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing book instances.
    Provides all CRUD operations: list, create, retrieve, update, destroy.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer