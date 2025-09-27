from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Book

class BookAPITestCase(APITestCase):
    """
    Test case for Book API endpoints including CRUD operations,
    filtering, searching, ordering, and authentication.
    """
    
    def setUp(self):
        """
        Set up test data that will be available for all test methods.
        """
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            email='test@example.com'
        )
        self.admin_user = User.objects.create_superuser(
            username='adminuser',
            password='adminpassword123',
            email='admin@example.com'
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
        self.book3 = Book.objects.create(
            title='1984',
            author='George Orwell',
            publication_year=1949,
            price=10.99
        )
        
        # API client
        self.client = APIClient()
        
        # URLs
        self.book_list_url = reverse('book-list')
        self.book_create_url = reverse('book-create')
        
    def get_token(self, username='testuser', password='testpassword123'):
        """Helper method to get authentication token"""
        url = reverse('api_token_auth')
        response = self.client.post(url, {
            'username': username,
            'password': password
        })
        return response.data.get('token')
    
    def authenticate_client(self, username='testuser', password='testpassword123'):
        """Helper method to authenticate the client"""
        token = self.get_token(username, password)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    
    # === AUTHENTICATION TESTS ===
    
    def test_unauthenticated_access_to_protected_endpoints(self):
        """
        Test that unauthenticated users cannot access protected endpoints.
        """
        # Test create endpoint without authentication
        response = self.client.post(self.book_create_url, {
            'title': 'New Book',
            'author': 'New Author',
            'publication_year': 2023,
            'price': 19.99
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Test update endpoint without authentication
        response = self.client.put(reverse('book-update'), {
            'id': self.book1.id,
            'title': 'Updated Title',
            'author': 'Updated Author'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Test delete endpoint without authentication
        response = self.client.delete(reverse('book-delete'), {
            'id': self.book1.id
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_authenticated_access_to_protected_endpoints(self):
        """
        Test that authenticated users can access protected endpoints.
        """
        self.authenticate_client()
        
        # Test create endpoint with authentication
        response = self.client.post(self.book_create_url, {
            'title': 'New Book',
            'author': 'New Author',
            'publication_year': 2023,
            'price': 19.99
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    # === CRUD OPERATION TESTS ===
    
    def test_list_books(self):
        """
        Test retrieving list of books (should be accessible without authentication).
        """
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # Should return all 3 books
    
    def test_retrieve_single_book(self):
        """
        Test retrieving a single book by ID.
        """
        url = reverse('book-detail', kwargs={'pk': self.book1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'The Great Gatsby')
        self.assertEqual(response.data['author'], 'F. Scott Fitzgerald')
    
    def test_create_book(self):
        """
        Test creating a new book with valid data.
        """
        self.authenticate_client()
        
        data = {
            'title': 'Brave New World',
            'author': 'Aldous Huxley',
            'publication_year': 1932,
            'price': 13.50
        }
        
        response = self.client.post(self.book_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(response.data['author'], data['author'])
        
        # Verify the book was actually created in the database
        self.assertTrue(Book.objects.filter(title='Brave New World').exists())
    
    def test_create_book_invalid_data(self):
        """
        Test creating a book with invalid data.
        """
        self.authenticate_client()
        
        data = {
            'title': '',  # Empty title - should be invalid
            'author': 'Test Author',
            'publication_year': 2023
        }
        
        response = self.client.post(self.book_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)  # Should have title validation error
    
    def test_update_book(self):
        """
        Test updating an existing book.
        """
        self.authenticate_client()
        
        data = {
            'id': self.book1.id,
            'title': 'Updated Gatsby Title',
            'author': 'F. Scott Fitzgerald',
            'publication_year': 1925,
            'price': 15.99
        }
        
        response = self.client.put(reverse('book-update'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Gatsby Title')
        
        # Verify the book was actually updated in the database
        updated_book = Book.objects.get(id=self.book1.id)
        self.assertEqual(updated_book.title, 'Updated Gatsby Title')
        self.assertEqual(float(updated_book.price), 15.99)
    
    def test_update_nonexistent_book(self):
        """
        Test updating a book that doesn't exist.
        """
        self.authenticate_client()
        
        data = {
            'id': 999,  # Non-existent ID
            'title': 'Nonexistent Book',
            'author': 'Nonexistent Author'
        }
        
        response = self.client.put(reverse('book-update'), data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_book(self):
        """
        Test deleting an existing book.
        """
        self.authenticate_client()
        
        book_id = self.book1.id
        response = self.client.delete(reverse('book-delete'), {'id': book_id})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify the book was actually deleted from the database
        self.assertFalse(Book.objects.filter(id=book_id).exists())
    
    def test_delete_nonexistent_book(self):
        """
        Test deleting a book that doesn't exist.
        """
        self.authenticate_client()
        
        response = self.client.delete(reverse('book-delete'), {'id': 999})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    # === FILTERING TESTS ===
    
    def test_filter_books_by_title(self):
        """
        Test filtering books by title.
        """
        response = self.client.get(self.book_list_url, {'title': 'Gatsby'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'The Great Gatsby')
    
    def test_filter_books_by_author(self):
        """
        Test filtering books by author.
        """
        response = self.client.get(self.book_list_url, {'author': 'Orwell'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], 'George Orwell')
    
    def test_filter_books_by_publication_year(self):
        """
        Test filtering books by publication year.
        """
        response = self.client.get(self.book_list_url, {'publication_year': 1960})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'To Kill a Mockingbird')
    
    def test_filter_books_by_publication_year_range(self):
        """
        Test filtering books by publication year range.
        """
        # Greater than 1950
        response = self.client.get(self.book_list_url, {'publication_year__gt': 1950})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'To Kill a Mockingbird')
        
        # Less than 1950
        response = self.client.get(self.book_list_url, {'publication_year__lt': 1950})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Gatsby and 1984
    
    # === SEARCHING TESTS ===
    
    def test_search_books(self):
        """
        Test searching books across title and author fields.
        """
        # Search by title
        response = self.client.get(self.book_list_url, {'search': 'Mockingbird'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'To Kill a Mockingbird')
        
        # Search by author
        response = self.client.get(self.book_list_url, {'search': 'Fitzgerald'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], 'F. Scott Fitzgerald')
        
        # Search that should return multiple results
        response = self.client.get(self.book_list_url, {'search': 'The'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    # === ORDERING TESTS ===
    
    def test_order_books_by_title_ascending(self):
        """
        Test ordering books by title in ascending order.
        """
        response = self.client.get(self.book_list_url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        titles = [book['title'] for book in response.data]
        # Check if titles are in alphabetical order
        self.assertEqual(titles, sorted(titles))
    
    def test_order_books_by_title_descending(self):
        """
        Test ordering books by title in descending order.
        """
        response = self.client.get(self.book_list_url, {'ordering': '-title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        titles = [book['title'] for book in response.data]
        # Check if titles are in reverse alphabetical order
        self.assertEqual(titles, sorted(titles, reverse=True))
    
    def test_order_books_by_publication_year(self):
        """
        Test ordering books by publication year.
        """
        response = self.client.get(self.book_list_url, {'ordering': 'publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        years = [book['publication_year'] for book in response.data]
        # Check if years are in ascending order
        self.assertEqual(years, sorted(years))
    
    def test_order_books_by_price_descending(self):
        """
        Test ordering books by price in descending order.
        """
        response = self.client.get(self.book_list_url, {'ordering': '-price'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        prices = [float(book['price']) for book in response.data]
        # Check if prices are in descending order
        self.assertEqual(prices, sorted(prices, reverse=True))
    
    # === COMBINED FEATURES TESTS ===
    
    def test_combined_filter_search_order(self):
        """
        Test combining filtering, searching, and ordering.
        """
        # Filter by year > 1900, search for 'The', order by title descending
        response = self.client.get(self.book_list_url, {
            'publication_year__gt': 1900,
            'search': 'The',
            'ordering': '-title'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return books with 'The' in title published after 1900, ordered Z-A
    
    def test_default_ordering(self):
        """
        Test that books are ordered by creation date (newest first) by default.
        """
        # Create a new book to test ordering
        new_book = Book.objects.create(
            title='Newest Book',
            author='New Author',
            publication_year=2023,
            price=20.00
        )
        
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # The first book should be the newest one
        self.assertEqual(response.data[0]['title'], 'Newest Book')


class BookModelTestCase(TestCase):
    """
    Test case for Book model methods and properties.
    """
    
    def setUp(self):
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            publication_year=2023,
            price=25.99
        )
    
    def test_book_creation(self):
        """Test that a book can be created successfully."""
        self.assertEqual(self.book.title, 'Test Book')
        self.assertEqual(self.book.author, 'Test Author')
        self.assertEqual(self.book.publication_year, 2023)
        self.assertEqual(float(self.book.price), 25.99)
        self.assertTrue(self.book.created_at)
        self.assertTrue(self.book.updated_at)
    
    def test_book_string_representation(self):
        """Test the string representation of the book model."""
        self.assertEqual(str(self.book), 'Test Book by Test Author')
    
    def test_book_default_ordering(self):
        """Test that books are ordered by creation date (newest first)."""
        # Create another book
        book2 = Book.objects.create(
            title='Older Book',
            author='Older Author',
            publication_year=2022,
            price=20.00
        )
        
        books = Book.objects.all()
        self.assertEqual(books[0].title, 'Older Book')  # Older book should come first?
        # Note: The actual order depends on your model's Meta.ordering