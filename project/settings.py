# -*- coding: utf-8 -*-
# Django global settings

# This allows us to construct the needed absolute paths dynamically,
# e.g., for the MEDIA_ROOT, and TEMPLATE_DIRS settings.
# see: http://rob.cogit8.org/blog/2008/Jun/20/django-and-relativity/
import os
import sys
normpath = lambda *args: os.path.normpath(os.path.abspath(os.path.join(*args)))
PROJECT_DIR = normpath(__file__, "..", "..")

sys.path.append(normpath(PROJECT_DIR, "project"))
sys.path.append(normpath(PROJECT_DIR, "apps"))

# http://docs.djangoproject.com/en/dev/topics/testing/#id1
# Your user must be a postgrest superuser
# Avoid specifying your password with: ~/.pgpass
# http://www.postgresql.org/docs/8.3/interactive/libpq-pgpass.html
TEST_RUNNER='django.contrib.gis.tests.run_gis_tests'

DEBUG = False
TEMPLATE_DEBUG = DEBUG

CACHES = {
	'default': {
		'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
		'LOCATION': '127.0.0.1:11211',
	},
}

LANGUAGE_CODE = 'cs-cz'

TIME_ZONE = 'Europe/Prague'

SITE_ID = 1

SITE_URL = 'http://www.zelenamapa.cz'

USE_I18N = True

MEDIA_ROOT = '/media/'
MEDIA_URL = '/media/'

STATIC_ROOT = '/static/'
STATIC_URL = '/static/'
LOGIN_URL = '/admin/'
STATICFILES_DIRS = (
        os.path.join(PROJECT_DIR, 'apps/mapa/static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
TEMPLATE_CONTEXT_PROCESSORS += (
     'django.core.context_processors.request',
     'django.core.context_processors.media',
     'django.contrib.messages.context_processors.messages',
     'constance.context_processors.config',
     'module.context_processors.site',
) 

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'mapwidget.middleware.crossdomainxhr.XsSharing',
    'author.middlewares.AuthorDefaultBackendMiddleware',
)

ROOT_URLCONF = 'urls'


# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'

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

    #for django_webmap_corpus:
    'author',
    'colorful',
    'adminsortable',
    'django.contrib.gis',
    'constance.backends.database',
    'constance',
    'import_export',
    'webmap',

    'easy_thumbnails',
    'compressor',
    'mapwidget',
    'django.contrib.sites',
    'fluent_comments',
    'crispy_forms',
    'django.contrib.comments',
    'massadmin',
    'comments_moderation',
    'mapa',
    'rest_framework',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
         'require_debug_false': {
             '()': 'django.utils.log.RequireDebugFalse'
         }
     },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': "/var/log/django/zm.log",
            'backupCount': 50,
            'maxBytes': 10000000,
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'logfile'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins', 'logfile'],
            'level': 'ERROR',
            'propagate': False,
        },
        'mapa': {
            'handlers': ['console', 'mail_admins', 'logfile'],
            'level': 'INFO',
        }
    }
}

CONSTANCE_APP_NAME = "webmap"
CONSTANCE_CONFIG = {
    'ENABLE_FEATURE_TIPY_ZM': (True, u'povolit tipy Zelené mapy v pravém sloupci'),
    'ENABLE_FEATURE_LEFT_POI_TIP': (True, u'povolit tip vlevo dole (True = poi vlevo dole je tip, False = poi vlevo dole je nahodny)'),
    'ENABLE_FEATURE_SOCIAL': (True, u'povolit sociální pluginy (Google+, Facebook, Twitter)'),
    'ENABLE_FEATURE_COMMENTS': (False, u'povolit komentáře k místům'),
    'ENABLE_FEATURE_WIDGET': (False, u'povolit widgetu k místům'),
    'MAP_BASEZOOM': (14, u'základní zoom mapy'),
    'MAP_POIZOOM': (17, u'zoom mapy pro zobrazení POI'),
    'MAP_BASELON': (14.4211, u'zeměpisná délka základní polohy mapy'),
    'MAP_BASELAT': (50.08741, u'zeměpisná délka základní polohy mapy'),
    'MAP_BOUNDS': ("14.22, 49.95, 14.8, 50.18", u'hranice zobrazení mapy'),
    'MIN_ZOOMLEVEL': (12, u'minimální zoomlevel mapy'),
    'DEFAULT_STATUS_ID': (13, u'id defaultního statusu'),
}
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

FLUENT_COMMENTS_EXCLUDE_FIELDS = ('url',)
COMMENTS_APP = 'fluent_comments'

COMPRESS_ENABLED=True

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'PAGINATE_BY': 10,                 # default to 10
    'PAGINATE_BY_PARAM': 'page_size',  # Allow client to override, using `?page_size=xxx`.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

# import local settings
try:
    from settings_local import *
except ImportError:
    pass
