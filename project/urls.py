from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
from django.urls import include, path
from django.contrib.sitemaps.views import sitemap
from django.contrib import admin
from django.contrib.auth import views as auth_views
import debug_toolbar

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

urlpatterns = [
    url(r'^admin/passreset/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^admin/passresetdone/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^admin/passresetconfirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^admin/passresetcomplete/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    url(r'^mapwidget/', include("mapwidget.urls")),
    url(r'^admin/', admin.site.urls),
    url(r'^admin/', include("massadmin.urls")),
    url(r'^comments/', include('fluent_comments.urls')),
    url(r'', include("mapa.urls")),
    # sitemap pro vyhledavace
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}),
    path('__debug__/', include(debug_toolbar.urls)),
]

urlpatterns += staticfiles_urlpatterns()
    
if settings.DEBUG:
    urlpatterns += [
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, show_indexes = True) \
      + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes = True) \
      + static('images', document_root=settings.MEDIA_ROOT + '/images', show_indexes = True)
