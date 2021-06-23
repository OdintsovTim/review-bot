from pathlib import Path

from configurations import Configuration, values


class BaseConfiguration(Configuration):
    BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent

    DOMAIN = values.Value()

    DEBUG = values.BooleanValue(True)
    LANGUAGE_CODE = values.Value('en-us')
    TIME_ZONE = values.Value('UTC')
    USE_I18N = values.BooleanValue(False)
    USE_L10N = values.BooleanValue(True)
    USE_TZ = values.BooleanValue(True)

    DATABASES = values.DatabaseURLValue('postgres://zip_user:zip_user@localhost:5432/botreview_db')

    ROOT_URLCONF = 'config.urls'
    WSGI_APPLICATION = 'config.wsgi.application'

    DJANGO_APPS = [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.admin',
    ]
    THIRD_PARTY_APPS = [
        'django_extensions',
    ]
    LOCAL_APPS = [
        'review_bot.review',
    ]
    INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    STATIC_ROOT = str(BASE_DIR / 'staticfiles')
    STATIC_URL = '/static/'
    STATICFILES_DIRS = [str(BASE_DIR / 'static')]

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [str(BASE_DIR / 'templates')],
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

    GITLAB_PRIVATE_TOKEN = values.SecretValue()
    GITLAB_API_VERSION = values.Value('v4')
    GITLAB_MAX_PAGINATOR_DEPTH = values.IntegerValue(20)
    GITLAB_WEBHOOK_URL = values.Value('gitlab/webhook/')
    GITLAB_GROUP_ID = values.IntegerValue()
    USE_GITLAB_SSL_VERIFICATION = values.BooleanValue(False)

    REVIEW_TIMEZONE = values.Value('Europe/Moscow')
