from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class ShelfBook(models.Model):
    """Model representing a book on a specific bookshelf."""
    
    bookshelf = models.ForeignKey(
        BookShelf,
        on_delete=models.CASCADE,
        related_name='shelf_books'
    )
    book = models.ForeignKey(
        'LibraryProject.relationship_app.Book',  # Update this line
        on_delete=models.CASCADE,
        related_name='shelf_entries'
    )
    added_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-added_at']
        unique_together = ['bookshelf', 'book']
    
    def __str__(self):
        return f"{self.book.title} on {self.bookshelf.name}"

class Author(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    
    def __str__(self):
        return self.title
    
    # ADD CUSTOM PERMISSIONS
    class Meta:
        permissions = [
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can change book"),
            ("can_delete_book", "Can delete book"),
        ]

class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, related_name='libraries')
    
    def __str__(self):
        return self.name

class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')
    
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Member')
    
    def __str__(self):
        return f"{self.user.email} - {self.role}"
    
class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""
    
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    """Custom User model with additional fields."""
    
    # Remove username field, use email instead
    username = None
    email = models.EmailField(_('email address'), unique=True)
    
    # Additional fields
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    
    # Set email as the unique identifier
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email & Password are required by default
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email

# Update the UserProfile model to use CustomUser
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)  # Updated to CustomUser
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Member')
    
    def __str__(self):
        return f"{self.user.email} - {self.role}"

# Update other models to use CustomUser if they reference User
class Author(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    
    def __str__(self):
        return self.title
    
    class Meta:
        permissions = [
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can change book"),
            ("can_delete_book", "Can delete book"),
        ]

class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, related_name='libraries')
    
    def __str__(self):
        return self.name

class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')
    
    def __str__(self):
        return self.name

# Update signals to use CustomUser
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()


# Signal to automatically create UserProfile when a new User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()