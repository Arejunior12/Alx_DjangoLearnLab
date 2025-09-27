from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model that includes all fields.
    Provides validation and data conversion between model and JSON.
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'created_at']  # Include all relevant fields
        
    def validate_title(self, value):
        """
        Custom validation for title field.
        Ensures title is not empty and has minimum length.
        """
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        if len(value) < 2:
            raise serializers.ValidationError("Title must be at least 2 characters long.")
        return value
    
    def validate_author(self, value):
        """
        Custom validation for author field.
        """
        if not value.strip():
            raise serializers.ValidationError("Author cannot be empty.")
        return value