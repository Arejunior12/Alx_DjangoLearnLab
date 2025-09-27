from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

# Generic Views for CRUD operations
class BookListView(generics.ListAPIView):
    """
    ListView for retrieving all books.
    AllowAny permission - anyone can view the book list.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single book by ID.
    AllowAny permission - anyone can view book details.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

class BookCreateView(generics.CreateAPIView):
    """
    CreateView for adding a new book.
    IsAuthenticated permission - only logged-in users can create books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView for modifying an existing book.
    IsAuthenticated permission - only logged-in users can update books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView for removing a book.
    IsAuthenticated permission - only logged-in users can delete books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

# Combined View for all CRUD operations (alternative approach)
class BookListCreateView(generics.ListCreateAPIView):
    """
    Combined view that handles both listing and creating books.
    Different permissions for different HTTP methods.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_permissions(self):
        """
        Custom permission handling:
        - GET: AllowAny (anyone can view)
        - POST: IsAuthenticated (only authenticated users can create)
        """
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Combined view that handles retrieve, update, and destroy operations.
    Different permissions for different HTTP methods.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_permissions(self):
        """
        Custom permission handling:
        - GET: AllowAny (anyone can view)
        - PUT/PATCH/DELETE: IsAuthenticated (only authenticated users can modify)
        """
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]