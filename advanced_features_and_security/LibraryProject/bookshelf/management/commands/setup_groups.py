import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.LibraryProject.settings')
import django
django.setup()

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from LibraryProject.bookshelf.models import Book

class Command(BaseCommand):
    help = 'Creates default groups and assigns permissions'

    def handle(self, *args, **options):
        # Get content type for Book model
        content_type = ContentType.objects.get_for_model(Book)
        
        # Get permissions
        can_view = Permission.objects.get(codename='can_view_book', content_type=content_type)
        can_create = Permission.objects.get(codename='can_create_book', content_type=content_type)
        can_edit = Permission.objects.get(codename='can_edit_book', content_type=content_type)
        can_delete = Permission.objects.get(codename='can_delete_book', content_type=content_type)

        # Create Groups
        viewers, created = Group.objects.get_or_create(name='Viewers')
        editors, created = Group.objects.get_or_create(name='Editors')
        admins, created = Group.objects.get_or_create(name='Admins')

        # Assign permissions to groups
        # Viewers can only view books
        viewers.permissions.set([can_view])
        
        # Editors can view, create, and edit books
        editors.permissions.set([can_view, can_create, can_edit])
        
        # Admins have all permissions
        admins.permissions.set([can_view, can_create, can_edit, can_delete])

        self.stdout.write(
            self.style.SUCCESS('Successfully created groups and assigned permissions')
        )