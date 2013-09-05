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
    (r'^$', mapa_view),
    (r'^misto/(\d+)/$', mapa_view),
    (r'^kml/([-\w]+)/$', kml_view),
    (r'^popup/(\d+)/$', popup_view),
    (r'^doplnit/(\d+)/$', 'mapa.views.addpoi_view'),
    (r'^doplnit/$', 'mapa.views.addpoi_view'),
    (r'^detail/(\d+)/', detail_view),
    (r'^vlastnosti/', vlastnosti_view),
    (r'^vrstvy/', vrstvy_view),
    (r'^znacky/', znacky_view),
    (r'^festival/(.*)', festival_view),
    (r'^search/([- \w]+)/$', search_view),
    (r'^admin/', include(admin.site.urls)),
    (r'^clanky/(.*)', static_view),
    # mobilni verze
    (r'^hledani/$', m_hledani),
    (r'^vypis/$', m_vypis),
    (r'^vypis/(\d+)/$', m_detail),
    # sitemap pro vyhledavace
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps})

)

urlpatterns += staticfiles_urlpatterns()
    
if settings.DEBUG:
    urlpatterns += patterns('',
    ) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, show_indexes = True) \
      + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes = True) \
      + static('images', document_root=settings.MEDIA_ROOT + '/images', show_indexes = True)
