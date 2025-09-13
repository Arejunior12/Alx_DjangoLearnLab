from django.contrib import admin
from .models import Book
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile, BookShelf, ShelfBook
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    """Define admin model for custom User model with no username field."""
    
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    
    list_display = ('email', 'is_staff', 'is_active', 'date_of_birth')
    list_filter = ('email', 'is_staff', 'is_active', 'date_of_birth')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'date_of_birth', 'profile_photo')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    
    search_fields = ('email',)
    ordering = ('email',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
    list_filter = ['role']

@admin.register(BookShelf)
class BookShelfAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'created_by__email']

@admin.register(ShelfBook)
class ShelfBookAdmin(admin.ModelAdmin):
    list_display = ['book', 'bookshelf', 'added_at']
    list_filter = ['added_at', 'bookshelf']

# Register the CustomUser model
admin.site.register(CustomUser, CustomUserAdmin)

class BookAdmin(admin.ModelAdmin):
    # Required: Display these fields in list view
    list_display = ('title', 'author', 'publication_year')
    
    # Required: Add filter options
    list_filter = ('publication_year', 'author')
    
    # Required: Add search functionality
    search_fields = ('title', 'author')

# Register the model with the custom admin class
admin.site.register(Book, BookAdmin)

@admin.register(BookShelf)
class BookShelfAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'created_by__email']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(ShelfBook)
class ShelfBookAdmin(admin.ModelAdmin):
    list_display = ['book', 'bookshelf', 'added_at']
    list_filter = ['added_at', 'bookshelf']
    search_fields = ['book__title', 'bookshelf__name']
    readonly_fields = ['added_at']