from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Library
from .models import Book

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

# Authentication views
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('relationship_app:list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


# Optional: Protect a view with login requirement
@login_required
def protected_view(request):
    return HttpResponse("This is a protected page!")