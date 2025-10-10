import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Determine the environment
ENVIRONMENT = os.environ.get('DJANGO_ENVIRONMENT', 'development')

if ENVIRONMENT == 'production':
    # Production settings
    DEBUG = False
    ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com', 'localhost', '127.0.0.1']
    
    # Security settings
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
else:
    # Development settings
    DEBUG = True
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Import the rest from base settings
if ENVIRONMENT == 'production':
    from .settings.production import *
else:
    from .settings.development import *