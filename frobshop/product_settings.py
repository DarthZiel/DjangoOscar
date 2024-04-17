import os
from dotenv import load_dotenv


load_dotenv()
ALLOWED_HOSTS = ['*']
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'django-insecure-$bm#eun%_qmrdgddgr@axc(7ag@k^$z8@owltosrh!x5o'
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '',
    }
}
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
