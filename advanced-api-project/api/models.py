from django.db import models

class Book(models.Model):
    """
    Book model with basic fields for demonstration.
    Includes timestamps for tracking creation and updates.
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.author}"

    class Meta:
        ordering = ['-created_at']  # Newest books first