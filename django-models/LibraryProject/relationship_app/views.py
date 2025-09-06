from django.shortcuts import render
from django.views.generic import DetailView
from django.http import HttpResponse
from .models import Book
from .models import Library

# Function-based view to list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view to display library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# Helper view to see available libraries
def library_list(request):
    libraries = Library.objects.all()
    response = "<h1>Available Libraries:</h1><ul>"
    for library in libraries:
        response += f'<li><a href="/relationship/library/{library.id}/">Library {library.id}: {library.name}</a></li>'
    response += "</ul>"
    return HttpResponse(response)