from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    """API view to list all books"""
    queryset = Book.objects.all()  # Get all book instances from the database
    serializer_class = BookSerializer  # Use the BookSerializer to convert to JSON