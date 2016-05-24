"""
Django settings for birthdaywidget project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import json
import socket
from cassandra import ConsistencyLevel

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

API_BASE = ""

try:

    vcap_app = json.loads(os.getenv("VCAP_APPLICATION"))
    API_BASE = vcap_app['application_uris'][0]

    print '>>>This computer name:', API_BASE

except Exception, e:
    print e
    pass

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_dw2pzl17xi#+lw0q&k%+qifl(bd^bd5cae9h$*2^c2fn-jb27'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',
    'birthdaywidget_app',
)
INSTALLED_APPS = ('django_cassandra_engine',) + INSTALLED_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
)

ROOT_URLCONF = 'birthdaywidget.urls'

WSGI_APPLICATION = 'birthdaywidget.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'cassandra': {
        'ENGINE':       'django_cassandra_engine',
        'NAME':         'yookos_upm',
        'TEST_NAME':    'test_ks_upm',
        'HOST':         '127.0.0.1',
        'OPTIONS': {
            'replication': {
                'strategy_class': 'SimpleStrategy',
                'replication_factor': 3
            }
        },
        'connection': {
                'consistency': ConsistencyLevel.ONE,
                'retry_connect': True,
                'lazy_connect': True
                # + All connection options for cassandra.cluster.Cluster()
            }
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Johannesburg'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/statics-files/

STATIC_URL = '/statics/'

STATIC_ROOT = '/statics/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'statics'),
)

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'birthdaywidget_app.pagination.CustomPagination',
    'PAGE_SIZE': 15
}

MEDIA_ROOT = '/static/media/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

EXCHANGE = 'birthday_exchange'

QUEUE = 'birthday_widget_queue'

RABBIT_HOST='localhost'

UPM_URL = 'http://upm.apps.yookore.net/api/v1/profile/'

PROD_DB = DEV_DB = False

if os.getenv('VCAP_SERVICES'):
    CLOUD_FOUNDRY = True
    vcap_app = json.loads(os.getenv("VCAP_APPLICATION"))

    platform = os.getenv("PLATFORM")

    print '>>>We are on:', platform

    if platform == 'DEV':
        DEV_DB = True
    else:
        PROD_DB = True
else:
    CLOUD_FOUNDRY = False

CLOUD_FOUNDRY = True
#
PROD_DB = True

if CLOUD_FOUNDRY:
    print "CF :", CLOUD_FOUNDRY
    if DEV_DB:
        print "DEV_DB"
        DATABASES['cassandra']['HOST']      = '192.168.10.200, 192.168.10.201, 192.168.10.202'
        DATABASES['cassandra']['USER']      = 'cassandra'
        DATABASES['cassandra']['PASSWORD']  = 'cassandra'

        RABBIT_USERNAME = 'test'
        RABBIT_PASSWORD = 'Wordpass15'
        RABBIT_HOST = '192.168.10.29'
        RABBIT_PORT = 5672

    elif PROD_DB:
        print "PROD_DB"
        DATABASES['cassandra']['HOST']      = '192.168.121.171, 192.168.121.172, 192.168.121.174, 192.168.121.175, 192.168.121.176'
        DATABASES['cassandra']['USER']      = 'cassandra'
        DATABASES['cassandra']['PASSWORD']  = 'Gonzo@7072'
        DATABASES['cassandra']['OPTIONS']['replication']['strategy_class'] = 'NetworkTopologyStrategy'
        DATABASES['cassandra']['OPTIONS']['replication']['DC1'] = 3

        UPM_URL = 'http://upm.apps.yookosapps.com/api/v1/profile/'
        RABBIT_USERNAME = 'yookore'
        RABBIT_PASSWORD = 'Wordpass15'
        RABBIT_HOST = '192.168.121.154'
        RABBIT_PORT = 5672

else:
    print "LOCAL"
    RABBIT_USERNAME = 'guest'
    RABBIT_PASSWORD = 'guest'
    RABBIT_HOST = 'localhost'
    RABBIT_PORT = 5672

    DATABASES['cassandra']['HOST']      = '127.0.0.1'

print '>>>Cassandra host:',DATABASES['cassandra']['HOST']
print '>>>Rabbit MQ host:',RABBIT_HOST


