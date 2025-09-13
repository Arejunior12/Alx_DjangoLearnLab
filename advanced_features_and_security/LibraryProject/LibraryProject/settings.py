import os
from pathlib import Path
import environ
from django.core.management.utils import get_random_secret_key

# Initialize environment variables
env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default=get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'csp',
    'LibraryProject.bookshelf',
    'LibraryProject.relationship_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'csp.middleware.CSPMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'LibraryProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'LibraryProject.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 12,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
AUTH_USER_MODEL = 'LibraryProject.bookshelf.CustomUser'

# Login redirects
LOGIN_REDIRECT_URL = '/relationship/books/'
LOGOUT_REDIRECT_URL = '/relationship/login/'

###############################################################################
# HTTPS AND SECURITY CONFIGURATION
###############################################################################

# HTTPS Settings - Enable these in production
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=False)
# When True, all non-HTTPS requests will be redirected to HTTPS
# Requires proper SSL certificate setup on the web server

# HTTP Strict Transport Security (HSTS)
SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', default=0)
# Set to 31536000 (1 year) for production
# HSTS tells browsers to only access the site via HTTPS for the specified time

SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=False)
# When True, HSTS policy applies to all subdomains

SECURE_HSTS_PRELOAD = env.bool('SECURE_HSTS_PRELOAD', default=False)
# When True, allows inclusion in browser preload lists

# Secure Cookies - Enable in production with HTTPS
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', default=False)
# When True, session cookies are only sent over HTTPS connections

CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', default=False)
# When True, CSRF cookies are only sent over HTTPS connections

SESSION_COOKIE_HTTPONLY = True
# When True, prevents JavaScript access to session cookies

CSRF_COOKIE_HTTPONLY = True
# When True, prevents JavaScript access to CSRF cookies

# Security Headers
X_FRAME_OPTIONS = 'DENY'
# Prevents clickjacking by denying framing of the site
# Options: 'DENY' (no framing), 'SAMEORIGIN' (same origin only), 'ALLOW-FROM uri'

SECURE_CONTENT_TYPE_NOSNIFF = True
# Prevents browsers from MIME-sniffing responses away from declared content-type
# Protects against MIME type confusion attacks

SECURE_BROWSER_XSS_FILTER = True
# Enables browser's built-in XSS protection
# Note: Modern browsers are deprecating this, but it's still good to include

SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
# Controls the Referer header in outbound links
# Options: 'no-referrer', 'same-origin', 'origin', 'strict-origin', etc.

# Content Security Policy (CSP)
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
CSP_IMG_SRC = ("'self'", "data:", "https:")
CSP_FONT_SRC = ("'self'",)
CSP_CONNECT_SRC = ("'self'",)
CSP_OBJECT_SRC = ("'none'",)
CSP_BASE_URI = ("'self'",)
CSP_FORM_ACTION = ("'self'",)
CSP_FRAME_ANCESTORS = ("'none'",)  # Equivalent to X-Frame-Options: DENY

# For development, you might need to adjust CSP for Django admin
if DEBUG:
    CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "'unsafe-eval'")
    CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")

# Proxy settings (if behind a reverse proxy)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# Uncomment if your Django app is behind a reverse proxy that handles SSL
# This tells Django to trust the X-Forwarded-Proto header from the proxy

# File upload security
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB