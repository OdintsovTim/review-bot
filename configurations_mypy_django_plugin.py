import os

from configurations import importer

from mypy_django_plugin.main import plugin  # noqa: F401

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

importer.install()
