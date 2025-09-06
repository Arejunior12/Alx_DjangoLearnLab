#!/usr/bin/env python
import os
import django
import sys

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set the Django settings module (adjust based on your actual project name)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')

# Setup Django
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def create_sample_data():
    """Create sample data for testing queries"""
    print("Creating sample data...")
    
    # Create authors
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="George R.R. Martin")
    author3 = Author.objects.create(name="Stephen King")
    
    # Create books
    book1 = Book.objects.create(title="Harry Potter and the Philosopher's Stone", author=author1)
    book2 = Book.objects.create(title="Harry Potter and the Chamber of Secrets", author=author1)
    book3 = Book.objects.create(title="A Game of Thrones", author=author2)
    book4 = Book.objects.create(title="A Clash of Kings", author=author2)
    book5 = Book.objects.create(title="The Shining", author=author3)
    book6 = Book.objects.create(title="It", author=author3)
    
    # Create libraries
    library1 = Library.objects.create(name="Central Library")
    library2 = Library.objects.create(name="City Public Library")
    
    # Add books to libraries
    library1.books.add(book1, book2, book3, book5)
    library2.books.add(book3, book4, book5, book6)
    
    # Create librarians
    librarian1 = Librarian.objects.create(name="Alice Johnson", library=library1)
    librarian2 = Librarian.objects.create(name="Bob Smith", library=library2)
    
    print("Sample data created successfully!\n")

def query_all_books_by_author(author_name):
    """Query all books by a specific author"""
    print(f"Query: All books by {author_name}")
    try:
        author = Author.objects.get(name=author_name)
        books = author.books.all()  # Using the related_name 'books'
        
        if books:
            print(f"Books by {author_name}:")
            for book in books:
                print(f"  - {book.title}")
        else:
            print(f"No books found for {author_name}")
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found")
    print()

def list_all_books_in_library(library_name):
    """List all books in a specific library"""
    print(f"Query: All books in {library_name}")
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        
        if books:
            print(f"Books in {library_name}:")
            for book in books:
                print(f"  - {book.title} (by {book.author.name})")
        else:
            print(f"No books found in {library_name}")
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found")
    print()

def retrieve_librarian_for_library(library_name):
    """Retrieve the librarian for a specific library"""
    print(f"Query: Librarian for {library_name}")
    try:
        library = Library.objects.get(name=library_name)
        librarian = library.librarian  # Using the related_name 'librarian'
        
        print(f"Librarian for {library_name}: {librarian.name}")
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found")
    except AttributeError:  # Changed from Librarian.DoesNotExist for OneToOne
        print(f"No librarian found for {library_name}")
    print()

def main():
    """Main function to demonstrate all queries"""
    # Create sample data first
    create_sample_data()
    
    # Demonstrate all the required queries
    print("=" * 50)
    print("DEMONSTRATING ADVANCED MODEL RELATIONSHIPS")
    print("=" * 50)
    
    # Query 1: All books by a specific author
    query_all_books_by_author("J.K. Rowling")
    
    # Query 2: All books in a library
    list_all_books_in_library("Central Library")
    
    # Query 3: Librarian for a library
    retrieve_librarian_for_library("Central Library")
    
    # Additional examples for demonstration
    query_all_books_by_author("George R.R. Martin")
    list_all_books_in_library("City Public Library")
    retrieve_librarian_for_library("City Public Library")

if __name__ == "__main__":
    main()