from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import patterns, url, include
from django.contrib import admin

from mapa.views import *
admin.autodiscover()

from django.contrib.sitemaps import Sitemap
from mapa.models import Poi

class MistaSitemap(Sitemap):
    def items(self):
        return Poi.viditelne.all()

sitemaps = {
        'mista': MistaSitemap
}

urlpatterns = patterns('',
    (r'^mapwidget/', include("mapwidget.urls")),
    (r'', include("mapa.urls")),
    # sitemap pro vyhledavace
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps})

)

urlpatterns += staticfiles_urlpatterns()
    
if settings.DEBUG:
    urlpatterns += patterns('',
    ) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, show_indexes = True) \
      + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes = True) \
      + static('images', document_root=settings.MEDIA_ROOT + '/images', show_indexes = True)
