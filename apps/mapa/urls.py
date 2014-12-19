from django.conf.urls import patterns

from mapa.views import mapa_view, popup_view, detail_view, vlastnosti_view, \
    znacky_view, festival_view, static_view, m_hledani, m_vypis, \
    m_detail, vrstvy_view

urlpatterns = patterns('',
                       (r'^$', mapa_view),
                       (r'^panel/$', mapa_view, {'template_name': 'panel.html'}),
                       (r'^layers/$', mapa_view, {'template_name': 'layers.js'}),
                       (r'^layers/(\d+)/$', mapa_view, {'template_name': 'layers.js'}),
                       (r'^misto/(\d+)/$', mapa_view),
                       (r'^popup/(\d+)/$', popup_view),
                       (r'^doplnit-form/(\d+)/$', 'mapa.views.addpoi_view', {'template_name': 'addpoi-form.html'}),
                       (r'^doplnit-form/$', 'mapa.views.addpoi_view', {'template_name': 'addpoi-form.html'}),
                       (r'^doplnit/(\d+)/$', 'mapa.views.addpoi_view'),
                       (r'^doplnit/$', 'mapa.views.addpoi_view'),
                       (r'^detail/(\d+)/', detail_view),
                       (r'^vlastnosti/', vlastnosti_view),
                       (r'^vrstvy/', vrstvy_view),
                       (r'^znacky/', znacky_view),
                       (r'^festival/(.*)', festival_view),
                       (r'^clanky/(.*)', static_view),
                       # mobilni verze
                       (r'^hledani/$', m_hledani),
                       (r'^vypis/$', m_vypis),
                       (r'^vypis/(\d+)/$', m_detail),
                       )
