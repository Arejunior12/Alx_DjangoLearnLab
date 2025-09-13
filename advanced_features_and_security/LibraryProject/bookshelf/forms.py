from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

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