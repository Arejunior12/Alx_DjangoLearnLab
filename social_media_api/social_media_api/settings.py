import os

# Check if we're in production or development
if os.environ.get('DJANGO_ENVIRONMENT') == 'production':
    from .settings.production import *
else:
    from .settings.development import *