from django.urls import path
from .views import list_books, LibraryDetailView, library_list  # CHANGE THIS LINE

app_name = 'relationship_app'

urlpatterns = [
    path('books/', list_books, name='list_books'),  # Changed from views.list_books
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),  # Changed from views.LibraryDetailView
    path('libraries/', library_list, name='library_list'),  # Changed from views.library_list
]