import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'django-insecure-$bm#eun%_qmgvi_+r#+xe5%@axc(7ag@k^$z8@owltosrh!x5o'


ALLOWED_HOSTS = ['*']

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tecno1',
        'USER': 'postgres',
        'PASSWORD': 'qaws1234',
        'HOST': 'localhost',
        'PORT': '',
    }
}
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')