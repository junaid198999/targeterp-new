import os
from .base import *  # noqa
from .base import env

DEBUG = env.bool('DJANGO_DEBUG', default=False)

SECRET_KEY = env('DJANGO_SECRET_KEY', default='Q6fN1C9TiFM0pKVAx49lGyaiD0EEymMK8BsReNDCiC2bKXw5AlTP6v7ryTF78dzZ')

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': env('DB_HOST', default='/cloudsql/' + env('CLOUD_SQL_CONNECTION', default='')),
        'NAME': env('DB_NAME', default='targeterp'),
        'USER': env('DB_USER', default='postgres'),
        'PASSWORD': env('DB_PASSWORD', default='TargetERP2024!'),
        'PORT': env('DB_PORT', default='5432'),
        'CONN_MAX_AGE': 60,
    }
}

if env('USE_CLOUD_SQL_PROXY', default='false') == 'true':
    DATABASES['default']['HOST'] = '127.0.0.1'

if env('CLOUD_SQL_CONNECTION', default=''):
    DATABASES['default']['HOST'] = '/cloudsql/' + env('CLOUD_SQL_CONNECTION')

DATABASES['default']['ATOMIC_REQUESTS'] = True

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

STATIC_ROOT = os.path.join(str(ROOT_DIR), 'staticfiles')
STATIC_URL = '/static/'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

MIGRATION_MODULES = {}
