from settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

DATABASES = {
        'default': {
                'ENGINE': 'django.contrib.gis.db.backends.postgis',
                'NAME': 'zelena_mapa',
                'USER': '',
                'PASSWORD': '',
                'HOST': 'localhost',
                'PORT': '',
        },
}

CACHES = {
	'default': {
		'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
		'LOCATION': '127.0.0.1:11211',
	},
}

LOGGING['handlers']['logfile']['filename'] = normpath(PROJECT_DIR, "zm.log")

MEDIA_ROOT = 'media/'

# DOPLNTE VLASTNI SECRET_KEY
SECRET_KEY = ''
