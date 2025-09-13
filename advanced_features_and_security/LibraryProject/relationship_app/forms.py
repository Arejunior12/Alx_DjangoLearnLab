from django import forms
from .models import Book, Author
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
        }
        
class CustomUserCreationForm(UserCreationForm):
    """Form for creating new users with custom fields."""
    
    class Meta:
        model = CustomUser
        fields = ('email', 'date_of_birth')

class CustomUserChangeForm(UserChangeForm):
    """Form for updating users with custom fields."""
    
    class Meta:
        model = CustomUser
        fields = ('email', 'date_of_birth', 'profile_photo')

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
        }