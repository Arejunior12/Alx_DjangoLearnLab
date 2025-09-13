from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
import re
from .models import CustomUser, Book

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

# ADD THE MISSING EXAMPLEFORM
class ExampleForm(forms.Form):
    """
    Example form demonstrating security best practices including:
    - Input validation
    - XSS prevention
    - CSRF protection (automatically included in Django forms)
    - Secure field types
    """
    
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your name',
            'pattern': '[A-Za-z\\s\\.\\-]+',  # Only letters, spaces, dots, hyphens
            'title': 'Only letters, spaces, dots, and hyphens allowed'
        }),
        error_messages={
            'required': 'Name is required',
            'max_length': 'Name cannot exceed 100 characters'
        }
    )
    
    email = forms.EmailField(
        max_length=150,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
        }),
        error_messages={
            'required': 'Email is required',
            'invalid': 'Please enter a valid email address'
        }
    )
    
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your message',
            'rows': 4,
            'maxlength': '1000'  # Client-side validation
        }),
        error_messages={
            'required': 'Message is required'
        }
    )
    
    age = forms.IntegerField(
        required=False,
        min_value=0,
        max_value=150,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your age (optional)',
            'min': '0',
            'max': '150'
        }),
        error_messages={
            'min_value': 'Age cannot be negative',
            'max_value': 'Age cannot exceed 150'
        }
    )
    
    website = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://example.com',
        }),
        error_messages={
            'invalid': 'Please enter a valid URL'
        }
    )
    
    agree_to_terms = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        }),
        error_messages={
            'required': 'You must agree to the terms and conditions'
        }
    )
    
    def clean_name(self):
        """Custom validation for name field to prevent XSS and injection"""
        name = self.cleaned_data.get('name', '').strip()
        
        # Check for empty name
        if not name:
            raise ValidationError("Name cannot be empty")
        
        # Prevent XSS by removing dangerous characters
        name = re.sub(r'[<>\"\']', '', name)
        
        # Validate name format (only letters, spaces, dots, hyphens)
        if not re.match(r'^[A-Za-z\s\.\-]+$', name):
            raise ValidationError("Name can only contain letters, spaces, dots, and hyphens")
        
        return name
    
    def clean_message(self):
        """Custom validation for message field"""
        message = self.cleaned_data.get('message', '').strip()
        
        if not message:
            raise ValidationError("Message cannot be empty")
        
        if len(message) < 10:
            raise ValidationError("Message must be at least 10 characters long")
        
        if len(message) > 1000:
            raise ValidationError("Message cannot exceed 1000 characters")
        
        # Basic XSS protection - remove script tags and dangerous attributes
        message = re.sub(r'<script.*?>.*?</script>', '', message, flags=re.IGNORECASE)
        message = re.sub(r'on\w+=\s*[\'\"].*?[\'\"]', '', message, flags=re.IGNORECASE)
        
        return message
    
    def clean_website(self):
        """Custom validation for website field"""
        website = self.cleaned_data.get('website', '').strip()
        
        if website:  # Only validate if provided
            # Ensure URL starts with http:// or https://
            if not website.startswith(('http://', 'https://')):
                raise ValidationError("URL must start with http:// or https://")
            
            # Basic domain validation
            if not re.match(r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', website):
                raise ValidationError("Please enter a valid website URL")
        
        return website
    
    def clean(self):
        """Form-wide validation"""
        cleaned_data = super().clean()
        
        # Example of cross-field validation
        age = cleaned_data.get('age')
        agree_to_terms = cleaned_data.get('agree_to_terms')
        
        if age and age < 13 and agree_to_terms:
            # For users under 13, we might need parental consent
            # This is just an example of complex validation logic
            pass
        
        return cleaned_data

class SecureSearchForm(forms.Form):
    """
    Secure search form with input validation to prevent SQL injection and XSS
    """
    
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search...',
            'pattern': '[A-Za-z0-9\\s\\.\\-\\,]+',
            'title': 'Only letters, numbers, spaces, and basic punctuation allowed'
        })
    )
    
    def clean_query(self):
        """Sanitize search query to prevent injection attacks"""
        query = self.cleaned_data.get('query', '').strip()
        
        if query:
            # Remove potentially dangerous characters
            query = re.sub(r'[;\"\'<>\(\)\-\-]', '', query)
            
            # Limit length for safety
            if len(query) > 100:
                raise ValidationError("Search query too long")
        
        return query