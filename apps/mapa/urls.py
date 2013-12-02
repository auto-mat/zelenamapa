from django.conf.urls import patterns

from mapa.views import *

urlpatterns = patterns('',
    (r'^$', mapa_view),
    (r'^misto/(\d+)/$', mapa_view),
    (r'^popup/(\d+)/$', popup_view),
    (r'^doplnit/(\d+)/$', 'mapa.views.addpoi_view'),
    (r'^doplnit/$', 'mapa.views.addpoi_view'),
    (r'^detail/(\d+)/', detail_view),
    (r'^vlastnosti/', vlastnosti_view),
    (r'^vrstvy/', vrstvy_view),
    (r'^znacky/', znacky_view),
    (r'^festival/(.*)', festival_view),
    (r'^search/([- \w]+)/$', search_view),
    (r'^clanky/(.*)', static_view),
    # mobilni verze
    (r'^hledani/$', m_hledani),
    (r'^vypis/$', m_vypis),
    (r'^vypis/(\d+)/$', m_detail),
)
