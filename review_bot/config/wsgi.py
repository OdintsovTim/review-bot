import os
from pathlib import Path

from configurations.wsgi import get_wsgi_application


ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Dev')

application = get_wsgi_application()
