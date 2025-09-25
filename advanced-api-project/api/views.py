from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

# Book Views - Using only correct DRF generic view classes
class BookListCreateView(generics.ListCreateAPIView):
    """
    ListCreateAPIView for listing all books or creating a new book.
    Handles GET (list) and POST (create) operations.
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year', 'author__name']
    ordering = ['title']
    
    def get_permissions(self):
        """Allow anyone to view, but only authenticated users to create"""
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    def list(self, request, *args, **kwargs):
        """Custom list response"""
        response = super().list(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'count': len(response.data),
            'data': response.data
        })
    
    def create(self, request, *args, **kwargs):
        """Custom create response"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            'status': 'success',
            'message': 'Book created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED, headers=headers)

class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    RetrieveUpdateDestroyAPIView for retrieve, update, and delete operations.
    Handles GET (retrieve), PUT/PATCH (update), and DELETE (delete) operations.
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    
    def get_permissions(self):
        """Allow anyone to view, but only authenticated users to modify"""
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    def retrieve(self, request, *args, **kwargs):
        """Custom retrieve response"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'status': 'success',
            'data': serializer.data
        })
    
    def update(self, request, *args, **kwargs):
        """Custom update response"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'status': 'success',
            'message': 'Book updated successfully',
            'data': serializer.data
        })
    
    def destroy(self, request, *args, **kwargs):
        """Custom delete response"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'status': 'success',
            'message': 'Book deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)

# Author Views - Using only correct DRF generic view classes
class AuthorListCreateView(generics.ListCreateAPIView):
    """
    ListCreateAPIView for listing all authors or creating a new author.
    Handles GET (list) and POST (create) operations.
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']
    
    def get_permissions(self):
        """Allow anyone to view, but only authenticated users to create"""
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    def list(self, request, *args, **kwargs):
        """Custom list response"""
        response = super().list(request, *args, **kwargs)
        return Response({
            'status': 'success',
            'count': len(response.data),
            'data': response.data
        })

class AuthorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    RetrieveUpdateDestroyAPIView for retrieve, update, and delete operations.
    Handles GET (retrieve), PUT/PATCH (update), and DELETE (delete) operations.
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    
    def get_permissions(self):
        """Allow anyone to view, but only authenticated users to modify"""
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    def destroy(self, request, *args, **kwargs):
        """Custom delete response with book count"""
        instance = self.get_object()
        book_count = instance.books.count()
        self.perform_destroy(instance)
        return Response({
            'status': 'success',
            'message': f'Author and {book_count} associated book(s) deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)