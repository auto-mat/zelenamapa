# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse

from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import get_current_site

from webmap.models import Poi
from constance import config

def map_view(request, pk, w, h, template="mapwidget/map.html"):
    obj = get_object_or_404(Poi, pk=pk)
    template_dict = {
        "obj": obj,
        "w": w,
        "h": h,
    }
    return render_to_response(template, template_dict, context_instance=RequestContext(request))

def mapconfig_js_view(request, pk, template="mapwidget/mapconfig.js"):
    obj = get_object_or_404(Poi, pk=pk)
    template_dict = {
        "obj": obj,
        'config' : config,
        'site': get_current_site(request).domain,
    }
    return render_to_response(template, template_dict, context_instance=RequestContext(request), mimetype="text/javascript")

def map_div_view(request, pk, w, h, template="mapwidget/map_div.html"):
    obj = get_object_or_404(Poi, pk=pk)
    template_dict = {
        "obj": obj,
        "w": w,
        "h": h,
        'site': get_current_site(request).domain,
    }
    return render_to_response(template, template_dict, context_instance=RequestContext(request), mimetype="text/plain")
