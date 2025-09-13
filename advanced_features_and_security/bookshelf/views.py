from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.db.models import Q
from django.core.exceptions import ValidationError
import re
from .models import Book
from .forms import ExampleForm, SecureSearchForm  # CORRECTED IMPORT

def sanitize_input(input_string):
    """Sanitize user input to prevent XSS and SQL injection"""
    if not input_string:
        return input_string
    
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>\"\']', '', input_string)
    return sanitized.strip()

# Book views with secure input handling
@permission_required('bookshelf.can_view_book', raise_exception=True)
def book_list(request):
    """View all books - with secure search functionality"""
    books = Book.objects.all()
    
    # Secure search functionality - parameterized query
    search_query = request.GET.get('q', '')
    if search_query:
        sanitized_query = sanitize_input(search_query)
        books = books.filter(
            Q(title__icontains=sanitized_query) | 
            Q(author__icontains=sanitized_query)
        )
    
    return render(request, 'bookshelf/book_list.html', {
        'books': books,
        'search_query': search_query,
    })

@permission_required('bookshelf.can_create_book', raise_exception=True)
def book_create(request):
    """Create a new book - with input validation"""
    if request.method == 'POST':
        try:
            # Sanitize and validate input
            title = sanitize_input(request.POST.get('title', ''))
            author = sanitize_input(request.POST.get('author', ''))
            
            # Validate input
            if not title or not author:
                return HttpResponseBadRequest("Title and author are required")
            
            if len(title) > 200:
                return HttpResponseBadRequest("Title too long")
            
            if len(author) > 100:
                return HttpResponseBadRequest("Author name too long")
            
            # Create book using ORM (safe from SQL injection)
            Book.objects.create(title=title, author=author)
            return redirect('bookshelf:book_list')
            
        except ValidationError as e:
            return HttpResponseBadRequest(f"Validation error: {e}")
        except Exception as e:
            return HttpResponseBadRequest(f"Error creating book: {e}")
    
    return render(request, 'bookshelf/book_form.html', {'action': 'Create'})

@permission_required('bookshelf.can_edit_book', raise_exception=True)
def book_edit(request, pk):
    """Edit a book - with secure input handling"""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        try:
            # Sanitize and validate input
            title = sanitize_input(request.POST.get('title', ''))
            author = sanitize_input(request.POST.get('author', ''))
            
            if not title or not author:
                return HttpResponseBadRequest("Title and author are required")
            
            # Update using ORM
            book.title = title
            book.author = author
            book.save()
            
            return redirect('bookshelf:book_list')
            
        except Exception as e:
            return HttpResponseBadRequest(f"Error updating book: {e}")
    
    return render(request, 'bookshelf/book_form.html', {'book': book, 'action': 'Edit'})

@permission_required('bookshelf.can_delete_book', raise_exception=True)
def book_delete(request, pk):
    """Delete a book - secure deletion"""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        try:
            book.delete()
            return redirect('bookshelf:book_list')
        except Exception as e:
            return HttpResponseBadRequest(f"Error deleting book: {e}")
    
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})

# Secure API view example
@login_required
def book_search_api(request):
    """Secure API endpoint for book search"""
    search_term = request.GET.get('q', '')
    
    if not search_term:
        return JsonResponse({'error': 'Search term required'}, status=400)
    
    # Sanitize input
    sanitized_term = sanitize_input(search_term)
    
    # Use parameterized ORM queries
    books = Book.objects.filter(
        Q(title__icontains=sanitized_term) | 
        Q(author__icontains=sanitized_term)
    ).values('id', 'title', 'author')[:10]  # Limit results
    
    return JsonResponse({'results': list(books)})

# ADD THESE NEW VIEWS THAT USE THE EXAMPLEFORM
@login_required
def example_form_view(request):
    """
    Example view demonstrating secure form handling
    with CSRF protection, input validation, and XSS prevention
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Process secure, validated data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # In a real application, you would save to database or send email
            # For demonstration, we'll just show a success message
            
            return render(request, 'bookshelf/example_form_success.html', {
                'name': name,
                'email': email,
            })
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/example_form.html', {'form': form})

@permission_required('bookshelf.can_view_book', raise_exception=True)
def secure_search(request):
    """
    Secure search view using form validation
    """
    form = SecureSearchForm(request.GET or None)
    books = Book.objects.all()
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        if query:
            # Use parameterized ORM query (safe from SQL injection)
            books = books.filter(
                Q(title__icontains=query) | 
                Q(author__icontains=query)
            )
    
    return render(request, 'bookshelf/secure_search.html', {
        'form': form,
        'books': books,
        'query': form.cleaned_data.get('query', '') if form.is_valid() else ''
    })