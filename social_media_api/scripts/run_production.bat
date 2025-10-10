@echo off
echo Setting production environment and starting server...

set DJANGO_ENVIRONMENT=production
set DEBUG=False

python manage.py runserver
pause