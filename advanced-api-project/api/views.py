from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

# Book Views - Using correct DRF generic view classes
class BookListView(generics.ListAPIView):
    """
    ListAPIView for retrieving all books with filtering and search capabilities.
    
    Provides read-only access to all Book instances with optional filtering
    by author, publication year, and search by title.
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year', 'author__name']
    ordering = ['title']

class BookDetailView(generics.RetrieveAPIView):
    """
    RetrieveAPIView for retrieving a single book by ID.
    
    Provides read-only access to a specific Book instance identified by primary key.
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

class BookCreateView(generics.CreateAPIView):
    """
    CreateAPIView for adding a new book with custom validation.
    
    Handles POST requests to create new Book instances with automatic
    validation using the BookSerializer.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateAPIView for modifying an existing book.
    
    Handles PUT and PATCH requests to update existing Book instances.
    Includes full validation and partial update support.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookDeleteView(generics.DestroyAPIView):
    """
    DestroyAPIView for removing a book from the database.
    
    Handles DELETE requests to remove Book instances permanently.
    Includes proper cascade deletion handling through foreign key relationships.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

# Combined View for Retrieve, Update, Delete operations
class BookRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    RetrieveUpdateDestroyAPIView for handling retrieve, update, and delete operations in one view.
    
    This combines the functionality of RetrieveAPIView, UpdateAPIView, and DestroyAPIView.
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Allow read for anyone, write for authenticated
    
    def get_permissions(self):
        """
        Customize permissions based on the HTTP method.
        """
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

# Author Views - Using correct DRF generic view classes
class AuthorListView(generics.ListAPIView):
    """
    ListAPIView for retrieving all authors with their related books.
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

class AuthorDetailView(generics.RetrieveAPIView):
    """
    RetrieveAPIView for retrieving a single author by ID with nested books.
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]

class AuthorCreateView(generics.CreateAPIView):
    """
    CreateAPIView for adding a new author.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]

class AuthorUpdateView(generics.UpdateAPIView):
    """
    UpdateAPIView for modifying an existing author.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]

class AuthorDeleteView(generics.DestroyAPIView):
    """
    DestroyAPIView for removing an author (cascades to related books).
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]

# Combined View for Author operations
class AuthorRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    RetrieveUpdateDestroyAPIView for handling all author operations in one view.
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]