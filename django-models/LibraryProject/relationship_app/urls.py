from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books, LibraryDetailView, library_list


app_name = 'relationship_app'

urlpatterns = [
    # Existing URLs
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('libraries/', library_list, name='library_list'),
    
    # Authentication URLs - USING DJANGO'S BUILT-IN VIEWS
    
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
]