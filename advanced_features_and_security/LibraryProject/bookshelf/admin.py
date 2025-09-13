from django.contrib import admin
from .models import Book
from .models import BookShelf, ShelfBook

class BookAdmin(admin.ModelAdmin):
    # Required: Display these fields in list view
    list_display = ('title', 'author', 'publication_year')
    
    # Required: Add filter options
    list_filter = ('publication_year', 'author')
    
    # Required: Add search functionality
    search_fields = ('title', 'author')

# Register the model with the custom admin class
admin.site.register(Book, BookAdmin)

@admin.register(BookShelf)
class BookShelfAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'created_by__email']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(ShelfBook)
class ShelfBookAdmin(admin.ModelAdmin):
    list_display = ['book', 'bookshelf', 'added_at']
    list_filter = ['added_at', 'bookshelf']
    search_fields = ['book__title', 'bookshelf__name']
    readonly_fields = ['added_at']