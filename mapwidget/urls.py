from django.conf.urls.defaults import patterns, include, url 
from django.views.generic.simple import direct_to_template
from django.views.generic.simple import redirect_to

from views import *

urlpatterns = patterns("",
    url(r"^(?P<pk>\d+)/$",
        map_view,
        name="zm.mapwidget.map", ),
    url(r"^mapconfig(?P<pk>\d+).js$",
        mapconfig_js_view,
        name="zm.mapwidget.map_js", ),
)