from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly

class BookCreateView(generics.CreateAPIView):
    """
    CreateView for adding a new book with enhanced customization.
    
    Features:
    - Custom validation hooks
    - Automatic author association
    - Response customization
    - Permission-based access control
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        """
        Custom method to handle book creation with additional logic.
        
        This hook is called when saving the new book instance and allows
        for custom processing before the object is saved to the database.
        """
        # Add custom logic here (e.g., logging, notifications)
        book = serializer.save()
        
        # Example: Log the creation activity
        print(f"Book '{book.title}' created by user {self.request.user}")
    
    def create(self, request, *args, **kwargs):
        """
        Custom create method to enhance response and validation.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Custom success response
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                'status': 'success',
                'message': 'Book created successfully',
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )

class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView for modifying an existing book with enhanced features.
    
    Features:
    - Partial update support (PATCH)
    - Custom validation
    - Audit trail capability
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_update(self, serializer):
        """
        Custom update method with additional business logic.
        """
        # Store original data for audit trail
        original_title = serializer.instance.title
        
        # Perform the update
        book = serializer.save()
        
        # Example: Log changes
        if original_title != book.title:
            print(f"Book title changed from '{original_title}' to '{book.title}'")
    
    def update(self, request, *args, **kwargs):
        """
        Custom update method with enhanced response handling.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(
            {
                'status': 'success',
                'message': 'Book updated successfully',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

# Custom Filter Class for Advanced Filtering
from django_filters import rest_framework as django_filters

class BookFilter(django_filters.FilterSet):
    """
    Custom filter class for advanced book filtering capabilities.
    """
    publication_year__gt = django_filters.NumberFilter(
        field_name='publication_year', 
        lookup_expr='gt',
        help_text="Filter books published after specified year"
    )
    publication_year__lt = django_filters.NumberFilter(
        field_name='publication_year', 
        lookup_expr='lt',
        help_text="Filter books published before specified year"
    )
    author_name = django_filters.CharFilter(
        field_name='author__name', 
        lookup_expr='icontains',
        help_text="Filter by author name (case-insensitive contains)"
    )
    
    class Meta:
        model = Book
        fields = ['author', 'publication_year']

class EnhancedBookListView(generics.ListAPIView):
    """
    Enhanced ListView with custom filtering and pagination.
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BookFilter  # Use custom filter class
    search_fields = ['title', 'author__name', '^title']  # '^' starts-with search
    ordering_fields = ['title', 'publication_year', 'author__name']
    ordering = ['title']
    
    # Custom pagination settings
    paginate_by = 10
    paginate_by_param = 'page_size'
    max_paginate_by = 100
    
class SecureBookCreateView(BookCreateView):
    """
    Book CreateView with enhanced permission controls.
    """
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

class SecureBookUpdateView(BookUpdateView):
    """
    Book UpdateView with object-level permissions.
    """
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

class SecureBookDeleteView(BookDeleteView):
    """
    Book DeleteView with admin-only permissions.
    """
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
