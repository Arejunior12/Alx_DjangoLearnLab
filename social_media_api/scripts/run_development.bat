@echo off
echo Setting development environment and starting server...

set DJANGO_ENVIRONMENT=development
set DEBUG=True

python manage.py runserver
pause