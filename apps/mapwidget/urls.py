from django.conf.urls import patterns, url

from views import map_view, map_div_view, mapconfig_js_view

urlpatterns = patterns("",
                       url(r"^(?P<w>\d+)x(?P<h>\d+)/(?P<pk>\d+)/$",
                           map_view,
                           name="zm.mapwidget.map", ),
                       url(r"^(?P<w>\d+)x(?P<h>\d+)/(?P<pk>\d+)/div/$",
                           map_div_view,
                           name="zm.mapwidget.map.div", ),
                       url(r"^mapconfig(?P<pk>\d+).js$",
                           mapconfig_js_view,
                           name="zm.mapwidget.map_js", ),
                       url(r"^mapconfig_div(?P<pk>\d+).js$",
                           mapconfig_js_view,
                           {"template": "mapwidget/mapconfig_div.js"},
                           name="zm.mapwidget.map_div_js", ),
                       )
