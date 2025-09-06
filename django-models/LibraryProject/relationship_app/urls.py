from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'relationship_app'

urlpatterns = [
    # Book and Library URLs
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    path('libraries/', views.library_list, name='library_list'),
    
    # Authentication URLs - EXACT FORMAT REQUIRED
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
]