from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

# Combined Book View that handles GET, PUT, PATCH, DELETE on same endpoint
class BookRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    RetrieveUpdateDestroyAPIView: Handles GET, PUT, PATCH, DELETE for books.
    
    This single view handles all operations on a specific book instance:
    - GET: Retrieve book details
    - PUT: Full update of book
    - PATCH: Partial update of book  
    - DELETE: Remove book
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    
    def get_permissions(self):
        """
        Dynamic permissions based on HTTP method.
        - Read operations (GET): Allow anyone
        - Write operations (PUT, PATCH, DELETE): Require authentication
        """
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    def retrieve(self, request, *args, **kwargs):
        """Custom retrieve method with enhanced response"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'status': 'success',
            'data': serializer.data
        })
    
    def update(self, request, *args, **kwargs):
        """Custom update method with enhanced response"""
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
        """Custom delete method with confirmation response"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'status': 'success',
            'message': 'Book deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)

# Combined Author View that handles GET, PUT, PATCH, DELETE on same endpoint
class AuthorRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    RetrieveUpdateDestroyAPIView: Handles GET, PUT, PATCH, DELETE for authors.
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    
    def get_permissions(self):
        """Dynamic permissions based on HTTP method"""
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    def destroy(self, request, *args, **kwargs):
        """Custom delete with books cascade handling"""
        instance = self.get_object()
        book_count = instance.books.count()
        self.perform_destroy(instance)
        return Response({
            'status': 'success',
            'message': f'Author and {book_count} associated books deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)

# Keep the individual views for List and Create operations
class BookListView(generics.ListAPIView):
    """ListAPIView: Handles GET for all books"""
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year', 'author__name']

class BookCreateView(generics.CreateAPIView):
    """CreateAPIView: Handles POST for new books"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class AuthorListView(generics.ListAPIView):
    """ListAPIView: Handles GET for all authors"""
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]

class AuthorCreateView(generics.CreateAPIView):
    """CreateAPIView: Handles POST for new authors"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]