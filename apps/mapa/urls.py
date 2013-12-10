from django.conf.urls import patterns

from mapa.views import mapa_view, popup_view, detail_view, vlastnosti_view, \
    znacky_view, festival_view, search_view, static_view, m_hledani, m_vypis, \
    m_detail, vrstvy_view

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
