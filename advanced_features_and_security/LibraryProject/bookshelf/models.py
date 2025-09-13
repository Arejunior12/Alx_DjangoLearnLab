from django.db import models
from django.conf import settings

class BookShelf(models.Model):
    """Model representing a bookshelf that can contain multiple books."""
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookshelves'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name

class ShelfBook(models.Model):
    """Model representing a book on a specific bookshelf."""
    
    bookshelf = models.ForeignKey(
        BookShelf,
        on_delete=models.CASCADE,
        related_name='shelf_books'
    )
    book = models.ForeignKey(
        'relationship_app.Book',
        on_delete=models.CASCADE,
        related_name='shelf_entries'
    )
    added_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-added_at']
        unique_together = ['bookshelf', 'book']
    
    def __str__(self):
        return f"{self.book.title} on {self.bookshelf.name}"

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    
    def __str__(self):
        return self.title