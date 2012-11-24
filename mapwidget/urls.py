from django.conf.urls.defaults import patterns, include, url 
from django.views.generic.simple import direct_to_template
from django.views.generic.simple import redirect_to

from views import *

urlpatterns = patterns("",
    url(r"^$",
    map_view,
    name="zm.mapwidget.map", ),
)