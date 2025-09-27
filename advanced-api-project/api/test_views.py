from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Book

class BookViewTests(APITestCase):
    """
    Unit tests for Book API views including CRUD operations,
    filtering, searching, ordering, and authentication.
    """
    
    def setUp(self):
        """Set up test data for all test methods."""
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        
        # Create test books
        self.book1 = Book.objects.create(
            title='The Great Gatsby',
            author='F. Scott Fitzgerald',
            publication_year=1925,
            price=12.99
        )
        self.book2 = Book.objects.create(
            title='To Kill a Mockingbird',
            author='Harper Lee',
            publication_year=1960,
            price=14.99
        )
        
        self.client = APIClient()
    
    def get_auth_token(self):
        """Helper to get authentication token."""
        url = reverse('api_token_auth')
        response = self.client.post(url, {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        return response.data.get('token')
    
    def authenticate_client(self):
        """Helper to authenticate the test client."""
        token = self.get_auth_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    
    # === AUTHENTICATION AND PERMISSION TESTS ===
    
    def test_unauthenticated_user_cannot_create_book(self):
        """Test that unauthenticated users cannot create books."""
        response = self.client.post(reverse('book-create'), {
            'title': 'New Book',
            'author': 'New Author'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_authenticated_user_can_create_book(self):
        """Test that authenticated users can create books."""
        self.authenticate_client()
        response = self.client.post(reverse('book-create'), {
            'title': 'New Book',
            'author': 'New Author',
            'publication_year': 2023,
            'price': 19.99
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_anyone_can_list_books(self):
        """Test that book listing is accessible without authentication."""
        response = self.client.get(reverse('book-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    # === CRUD OPERATION TESTS ===
    
    def test_create_book(self):
        """Test creating a new book with valid data."""
        self.authenticate_client()
        data = {
            'title': 'Brave New World',
            'author': 'Aldous Huxley',
            'publication_year': 1932,
            'price': 13.50
        }
        response = self.client.post(reverse('book-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(response.data['title'], 'Brave New World')
    
    def test_retrieve_book(self):
        """Test retrieving a single book by ID."""
        response = self.client.get(reverse('book-detail', kwargs={'pk': self.book1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'The Great Gatsby')
    
    def test_update_book(self):
        """Test updating an existing book."""
        self.authenticate_client()
        data = {
            'id': self.book1.id,
            'title': 'Updated Title',
            'author': 'F. Scott Fitzgerald',
            'publication_year': 1925,
            'price': 15.99
        }
        response = self.client.put(reverse('book-update'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Title')
    
    def test_delete_book(self):
        """Test deleting a book."""
        self.authenticate_client()
        response = self.client.delete(reverse('book-delete'), {'id': self.book1.id})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)
    
    # === FILTERING TESTS ===
    
    def test_filter_books_by_title(self):
        """Test filtering books by title."""
        response = self.client.get(reverse('book-list'), {'title': 'Gatsby'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'The Great Gatsby')
    
    def test_filter_books_by_author(self):
        """Test filtering books by author."""
        response = self.client.get(reverse('book-list'), {'author': 'Lee'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], 'Harper Lee')
    
    def test_filter_books_by_publication_year(self):
        """Test filtering books by publication year."""
        response = self.client.get(reverse('book-list'), {'publication_year': 1960})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['publication_year'], 1960)
    
    # === SEARCHING TESTS ===
    
    def test_search_books_by_title(self):
        """Test searching books by title."""
        response = self.client.get(reverse('book-list'), {'search': 'Mockingbird'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'To Kill a Mockingbird')
    
    def test_search_books_by_author(self):
        """Test searching books by author."""
        response = self.client.get(reverse('book-list'), {'search': 'Fitzgerald'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], 'F. Scott Fitzgerald')
    
    # === ORDERING TESTS ===
    
    def test_order_books_by_title_ascending(self):
        """Test ordering books by title ascending."""
        response = self.client.get(reverse('book-list'), {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))
    
    def test_order_books_by_title_descending(self):
        """Test ordering books by title descending."""
        response = self.client.get(reverse('book-list'), {'ordering': '-title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles, reverse=True))
    
    def test_order_books_by_publication_year(self):
        """Test ordering books by publication year."""
        response = self.client.get(reverse('book-list'), {'ordering': 'publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years))
    
    # === ERROR HANDLING TESTS ===
    
    def test_create_book_invalid_data(self):
        """Test creating a book with invalid data."""
        self.authenticate_client()
        response = self.client.post(reverse('book-create'), {
            'title': '',  # Empty title should be invalid
            'author': 'Test Author'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_nonexistent_book(self):
        """Test updating a book that doesn't exist."""
        self.authenticate_client()
        response = self.client.put(reverse('book-update'), {
            'id': 999,  # Non-existent ID
            'title': 'Nonexistent Book'
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_nonexistent_book(self):
        """Test deleting a book that doesn't exist."""
        self.authenticate_client()
        response = self.client.delete(reverse('book-delete'), {'id': 999})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_retrieve_nonexistent_book(self):
        """Test retrieving a book that doesn't exist."""
        response = self.client.get(reverse('book-detail', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BookModelTests(TestCase):
    """Tests for the Book model."""
    
    def test_create_book_model(self):
        """Test creating a Book model instance."""
        book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            publication_year=2023,
            price=25.99
        )
        self.assertEqual(book.title, 'Test Book')
        self.assertEqual(book.author, 'Test Author')
        self.assertEqual(book.publication_year, 2023)
        self.assertEqual(float(book.price), 25.99)
    
    def test_book_string_representation(self):
        """Test the string representation of Book model."""
        book = Book.objects.create(
            title='Test Book',
            author='Test Author'
        )
        self.assertEqual(str(book), 'Test Book by Test Author')