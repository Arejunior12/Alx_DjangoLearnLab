# Permissions and Groups Setup Guide

## Overview
This application uses Django's built-in permission system with custom permissions for the Book model.

## Custom Permissions
- `can_view_book`: View book listings
- `can_create_book`: Create new books
- `can_edit_book`: Edit existing books
- `can_delete_book`: Delete books

## Groups
1. **Viewers**: Can view books only
2. **Editors**: Can view, create, and edit books
3. **Admins**: Full permissions (view, create, edit, delete)

## Setup Commands
```bash
# Create migrations and apply
python manage.py makemigrations
python manage.py migrate

# Setup default groups and permissions
python manage.py setup_groups

# Create test users
python manage.py createsuperuser