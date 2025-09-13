import os
from dotenv import load_dotenv

# Load environment variables based on environment
if os.path.exists('.env.production'):
    load_dotenv('.env.production')
else:
    load_dotenv('.env.development')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.LibraryProject.settings')

application = get_wsgi_application()