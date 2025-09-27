from rest_framework import generics, permissions, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

class BookListView(generics.ListAPIView):
    """
    Book List View with advanced filtering, searching, and ordering capabilities.
    
    Filtering Examples:
    - /books/?title=harry                    (books with 'harry' in title)
    - /books/?author=tolkien                 (books by Tolkien)
    - /books/?publication_year=2001          (books published in 2001)
    - /books/?publication_year__gt=2000      (books after 2000)
    - /books/?publication_year__lt=2010      (books before 2010)
    
    Search Examples:
    - /books/?search=harry potter            (search in title and author)
    
    Ordering Examples:
    - /books/?ordering=title                 (A-Z by title)
    - /books/?ordering=-title                (Z-A by title)
    - /books/?ordering=publication_year      (oldest first)
    - /books/?ordering=-publication_year     (newest first)
    - /books/?ordering=price                 (cheapest first)
    - /books/?ordering=-price                (most expensive first)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    
    # Filtering, Searching, and Ordering Configuration
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'author', 'publication_year']  # Simple filtering
    search_fields = ['title', 'author']  # Fields to search in
    ordering_fields = ['title', 'author', 'publication_year', 'price', 'created_at']  # Fields to order by
    ordering = ['-created_at']  # Default ordering (newest first)

class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

# Special function-based views for the exact URL patterns without pk
@api_view(['PUT'])
def update_book(request):
    book_id = request.data.get('id')
    book = get_object_or_404(Book, id=book_id)
    serializer = BookSerializer(book, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_book(request):
    book_id = request.data.get('id')
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return Response(status=204)