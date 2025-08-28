from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    # Required: Display these fields in list view
    list_display = ('title', 'author', 'publication_year')
    
    # Required: Add filter options
    list_filter = ('publication_year', 'author')
    
    # Required: Add search functionality
    search_fields = ('title', 'author')

# Register the model with the custom admin class
admin.site.register(Book, BookAdmin)