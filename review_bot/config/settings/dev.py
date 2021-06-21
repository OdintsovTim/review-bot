from configurations import values

from .base import BaseConfiguration  # noqa: ABS101, I252


class Dev(BaseConfiguration):
    DEBUG = True

    SECRET_KEY = values.SecretValue()
    ALLOWED_HOSTS = ['*']
