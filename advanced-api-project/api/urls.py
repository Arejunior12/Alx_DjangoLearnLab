from django.urls import path
from . import views

urlpatterns = [
    # Book URLs - Individual views
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
    
    # Book URLs - Combined view (alternative approach)
    path('books/<int:pk>/manage/', views.BookRetrieveUpdateDeleteView.as_view(), name='book-manage'),
    
    # Author URLs - Individual views
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('authors/create/', views.AuthorCreateView.as_view(), name='author-create'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('authors/<int:pk>/update/', views.AuthorUpdateView.as_view(), name='author-update'),
    path('authors/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name='author-delete'),
    
    # Author URLs - Combined view (alternative approach)
    path('authors/<int:pk>/manage/', views.AuthorRetrieveUpdateDeleteView.as_view(), name='author-manage'),
]