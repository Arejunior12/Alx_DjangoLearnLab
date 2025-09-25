from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class BookListAPIView(generics.ListAPIView):
    """
    ListAPIView for retrieving all books.
    Handles GET requests to list book resources.
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year', 'author__name']
    ordering = ['title']


class BookCreateAPIView(generics.CreateAPIView):
    """
    CreateAPIView for creating new books.
    Handles POST requests to create book resources.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookRetrieveAPIView(generics.RetrieveAPIView):
    """
    RetrieveAPIView for retrieving single books.
    Handles GET requests for individual book resources.
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookUpdateAPIView(generics.UpdateAPIView):
    """
    UpdateAPIView for updating existing books.
    Handles PUT and PATCH requests to update book resources.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookDestroyAPIView(generics.DestroyAPIView):
    """
    DestroyAPIView for deleting books.
    Handles DELETE requests to remove book resources.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


# Combined views for more efficient endpoints
class BookListCreateAPIView(generics.ListCreateAPIView):
    """
    ListCreateAPIView for listing and creating books.
    Combines ListAPIView and CreateAPIView functionality.
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year', 'author__name']
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    RetrieveUpdateDestroyAPIView for retrieve, update, delete operations.
    Combines RetrieveAPIView, UpdateAPIView, and DestroyAPIView functionality.
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


# Author Views
class AuthorListAPIView(generics.ListAPIView):
    """
    ListAPIView for retrieving all authors.
    Handles GET requests to list author resources.
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']


class AuthorCreateAPIView(generics.CreateAPIView):
    """
    CreateAPIView for creating new authors.
    Handles POST requests to create author resources.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]


class AuthorRetrieveAPIView(generics.RetrieveAPIView):
    """
    RetrieveAPIView for retrieving single authors.
    Handles GET requests for individual author resources.
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]


class AuthorUpdateAPIView(generics.UpdateAPIView):
    """
    UpdateAPIView for updating existing authors.
    Handles PUT and PATCH requests to update author resources.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]


class AuthorDestroyAPIView(generics.DestroyAPIView):
    """
    DestroyAPIView for deleting authors.
    Handles DELETE requests to remove author resources.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]


# Combined Author Views
class AuthorListCreateAPIView(generics.ListCreateAPIView):
    """
    ListCreateAPIView for listing and creating authors.
    Combines ListAPIView and CreateAPIView functionality.
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class AuthorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    RetrieveUpdateDestroyAPIView for retrieve, update, delete operations.
    Combines RetrieveAPIView, UpdateAPIView, and DestroyAPIView functionality.
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]