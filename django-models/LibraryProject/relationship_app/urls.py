from django.urls import path
from LibraryProject.relationship_app import views  # Updated import

app_name = 'relationship_app'

urlpatterns = [
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    path('libraries/', views.library_list, name='library_list'),  # Added this line
]