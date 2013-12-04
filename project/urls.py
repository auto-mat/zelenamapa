from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from mapa.views import *
admin.autodiscover()

from django.contrib.sitemaps import Sitemap
from webmap.models import Poi

class MistaSitemap(Sitemap):
    def items(self):
        return Poi.visible.all()

sitemaps = {
        'mista': MistaSitemap
}

urlpatterns = patterns('',
    url(r'^admin/passreset/$',auth_views.password_reset,name='password_reset'),
    url(r'^admin/passresetdone/$',auth_views.password_reset_done,name='password_reset_done'),
    url(r'^admin/passresetconfirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',auth_views.password_reset_confirm,name='password_reset_confirm'),
    url(r'^admin/passresetcomplete/$',auth_views.password_reset_complete,name='password_reset_complete'),
    (r'^mapwidget/', include("mapwidget.urls")),
    (r'^admin/', include(admin.site.urls)),
    url(r'^admin/', include("massadmin.urls")),
    url(r'^comments/', include('fluent_comments.urls')),
    url(r'^webmap/', include('webmap.urls')),
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
