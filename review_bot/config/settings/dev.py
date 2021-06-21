from configurations import values

from review_bot.config.settings.base import BaseConfiguration


class Dev(BaseConfiguration):
    DEBUG = True

    SECRET_KEY = values.SecretValue()
    ALLOWED_HOSTS = ['*']
