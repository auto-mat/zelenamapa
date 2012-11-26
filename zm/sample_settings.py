# Django global settings

# This allows us to construct the needed absolute paths dynamically,
# e.g., for the MEDIA_ROOT, and TEMPLATE_DIRS settings.
# see: http://rob.cogit8.org/blog/2008/Jun/20/django-and-relativity/
import os
PROJECT_DIR = os.path.dirname(__file__)

# http://docs.djangoproject.com/en/dev/topics/testing/#id1
# Your user must be a postgrest superuser
# Avoid specifying your password with: ~/.pgpass
# http://www.postgresql.org/docs/8.3/interactive/libpq-pgpass.html
TEST_RUNNER='django.contrib.gis.tests.run_gis_tests'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

DATABASES = {
        'default': {
                'ENGINE': 'django.contrib.gis.db.backends.postgis',
                'NAME': '',
                'USER': '',
                'PASSWORD': '',
                'HOST': 'localhost',
                'PORT': '',
        },
}

CACHES = {
	'default': {
		'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
#		'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
		'LOCATION': '127.0.0.1:11211',
	},
}

LANGUAGE_CODE = 'cs-cz'

TIME_ZONE = 'Europe/Prague'

SITE_ID = 1

SITE_URL = 'http://www.zelenamapa.cz'

USE_I18N = True

MEDIA_ROOT = '/home/www/zelenamapa.cz/media/'
MEDIA_URL = '/media/'

STATIC_ROOT = '/home/www/zelenamapa.cz/static/'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
        os.path.join(PROJECT_DIR, 'static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)


# DOPLNTE VLASTNI SECRET_KEY
SECRET_KEY = ''

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
TEMPLATE_CONTEXT_PROCESSORS += (
     'django.core.context_processors.request',
     'django.core.context_processors.media',
     'django.contrib.messages.context_processors.messages',
     'module.context_processors.site',
) 

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'mapwidget.middleware.crossdomainxhr.XsSharing',
)

ROOT_URLCONF = 'zm.urls'


# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'zm.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
    os.path.join(PROJECT_DIR, 'olwidget/templates'),
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'mapa',
    'easy_thumbnails',
    'compressor',
    'mapwidget',
    'south',
    'comment',
)
