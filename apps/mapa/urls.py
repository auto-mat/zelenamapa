from django.conf.urls import url 

from mapa.views import *

urlpatterns = [
    url(r'^$', mapa_view),
    url(r'^misto/(\d+)/$', mapa_view, name="mapa.views.mapa_view"),
    url(r'^kml/([-\w]+)/$', kml_view, name="mapa.views.kml_view"),
    url(r'^popup/(\d+)/$', popup_view, name="mapa.views.popup_view"),
    url(r'^doplnit/(\d+)/$', addpoi_view, name="mapa.views.addpoi_view"),
    url(r'^doplnit/$', addpoi_view, name="mapa.views.addpoi_view"),
    url(r'^detail/(\d+)/', detail_view, name="mapa.views.detail_view"),
    url(r'^vlastnosti/', vlastnosti_view, name="mapa.views.vlastnosti_view"),
    url(r'^vrstvy/', vrstvy_view, name="mapa.views.vrstvy_view"),
    url(r'^znacky/', znacky_view, name="mapa.views.znacky_view"),
    url(r'^festival/(.*)', festival_view, name="mapa.views.festival_view"),
    url(r'^search/([- \w]+)/$', search_view, name="mapa.views.search_view"),
    url(r'^clanky/(.*)', static_view, name="mapa.views.static_view"),
    # mobilni verze
    url(r'^hledani/$', m_hledani, name="mapa.views.m_hledani"),
    url(r'^vypis/$', m_vypis, name="mapa.views.m_vypis"),
    url(r'^vypis/(\d+)/$', m_detail, name="mapa.views.m_detail"),
]
