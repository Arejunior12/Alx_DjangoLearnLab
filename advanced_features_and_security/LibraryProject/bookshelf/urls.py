from django.urls import path
from . import views

app_name = 'bookshelf'

urlpatterns = [
    path('books/', views.book_list, name='book_list'),
    path('books/create/', views.book_create, name='book_create'),
    path('books/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
    path('permission-dashboard/', views.permission_dashboard, name='permission_dashboard'),
    
    # ADD THESE NEW PATHS
    path('example-form/', views.example_form_view, name='example_form'),
    path('secure-search/', views.secure_search, name='secure_search'),
]