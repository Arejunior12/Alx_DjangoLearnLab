import os
import django
from django.test import TestCase
from django.contrib.auth.models import User

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
django.setup()

from api.models import Author, Book

def create_test_data():
    """Create test data for manual testing"""
    
    # Create test author
    author, created = Author.objects.get_or_create(
        name="George Orwell",
        defaults={'name': 'George Orwell'}
    )
    
    # Create test books
    book1, created = Book.objects.get_or_create(
        title="1984",
        defaults={
            'title': '1984',
            'publication_year': 1949,
            'author': author
        }
    )
    
    book2, created = Book.objects.get_or_create(
        title="Animal Farm",
        defaults={
            'title': 'Animal Farm',
            'publication_year': 1945,
            'author': author
        }
    )
    
    print("Test data created successfully!")
    print(f"Author: {author.name}")
    print(f"Books: {book1.title} ({book1.publication_year}), {book2.title} ({book2.publication_year})")

if __name__ == "__main__":
    create_test_data()