from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    """API view to list all books - Public read access"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  # Allow anyone to view books

class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing book instances.
    Requires authentication for all operations.
    Admin users have full access, regular users can only view.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['list', 'retrieve']:
            # Allow any authenticated user to view books
            permission_classes = [IsAuthenticated]
        else:
            # Only admin users can create, update, or delete books
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]