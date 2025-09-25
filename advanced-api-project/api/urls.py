from django.urls import path
from . import views

# Option 1: Separate views for maximum control
urlpatterns = [
    # Book endpoints - separate views
    path('books/', views.BookListAPIView.as_view(), name='book-list'),
    path('books/create/', views.BookCreateAPIView.as_view(), name='book-create'),
    path('books/<int:pk>/', views.BookRetrieveAPIView.as_view(), name='book-retrieve'),
    path('books/<int:pk>/update/', views.BookUpdateAPIView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', views.BookDestroyAPIView.as_view(), name='book-destroy'),
    
    # Author endpoints - separate views
    path('authors/', views.AuthorListAPIView.as_view(), name='author-list'),
    path('authors/create/', views.AuthorCreateAPIView.as_view(), name='author-create'),
    path('authors/<int:pk>/', views.AuthorRetrieveAPIView.as_view(), name='author-retrieve'),
    path('authors/<int:pk>/update/', views.AuthorUpdateAPIView.as_view(), name='author-update'),
    path('authors/<int:pk>/delete/', views.AuthorDestroyAPIView.as_view(), name='author-destroy'),
]
