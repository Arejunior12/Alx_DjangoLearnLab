from django.urls import path
from . import views

urlpatterns = [
    # Book URLs - Using the combined RetrieveUpdateDestroyAPIView approach
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/', views.BookRetrieveUpdateDeleteView.as_view(), name='book-detail'),
    
    # Alternative: Separate endpoints for each operation (if preferred)
    # path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    # path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    # path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
    
    # Author URLs - Using the combined RetrieveUpdateDestroyAPIView approach
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('authors/create/', views.AuthorCreateView.as_view(), name='author-create'),
    path('authors/<int:pk>/', views.AuthorRetrieveUpdateDeleteView.as_view(), name='author-detail'),
    
    # Alternative: Separate endpoints for each operation (if preferred)
    # path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    # path('authors/<int:pk>/update/', views.AuthorUpdateView.as_view(), name='author-update'),
    # path('authors/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name='author-delete'),
]