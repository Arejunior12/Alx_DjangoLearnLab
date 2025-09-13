from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, JsonResponse
from .models import Book

# Book views with permission checks
@permission_required('bookshelf.can_view_book', raise_exception=True)
def book_list(request):
    """View all books - requires can_view_book permission"""
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@permission_required('bookshelf.can_create_book', raise_exception=True)
def book_create(request):
    """Create a new book - requires can_create_book permission"""
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        if title and author:
            Book.objects.create(title=title, author=author)
            return redirect('book_list')
    return render(request, 'bookshelf/book_form.html', {'action': 'Create'})

@permission_required('bookshelf.can_edit_book', raise_exception=True)
def book_edit(request, pk):
    """Edit a book - requires can_edit_book permission"""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.save()
        return redirect('book_list')
    return render(request, 'bookshelf/book_form.html', {'book': book, 'action': 'Edit'})

@permission_required('bookshelf.can_delete_book', raise_exception=True)
def book_delete(request, pk):
    """Delete a book - requires can_delete_book permission"""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})

# Dashboard view to show user permissions
@login_required
def permission_dashboard(request):
    """Show user's permissions and group membership"""
    user = request.user
    groups = user.groups.all()
    permissions = user.get_all_permissions()
    
    return render(request, 'bookshelf/permission_dashboard.html', {
        'user': user,
        'groups': groups,
        'permissions': permissions,
    })