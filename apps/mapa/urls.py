from django.conf.urls import url 

from mapa.views import *

urlpatterns = [
    url(r'^$', mapa_view),
    url(r'^misto/(\d+)/$', mapa_view),
    url(r'^kml/([-\w]+)/$', kml_view),
    url(r'^popup/(\d+)/$', popup_view),
    url(r'^doplnit/(\d+)/$', addpoi_view),
    url(r'^doplnit/$', addpoi_view),
    url(r'^detail/(\d+)/', detail_view),
    url(r'^vlastnosti/', vlastnosti_view),
    url(r'^vrstvy/', vrstvy_view),
    url(r'^znacky/', znacky_view),
    url(r'^festival/(.*)', festival_view),
    url(r'^search/([- \w]+)/$', search_view),
    url(r'^clanky/(.*)', static_view),
    # mobilni verze
    url(r'^hledani/$', m_hledani),
    url(r'^vypis/$', m_vypis),
    url(r'^vypis/(\d+)/$', m_detail),
]
