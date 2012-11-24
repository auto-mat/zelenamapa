# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse

from django.db.models import Q
from django.contrib.auth.decorators import login_required

from mapa.models import Poi

def map_view(request, pk, template="mapwidget/map.html"):
    obj = get_object_or_404(Poi, pk=pk)
    template_dict = {
        "obj": obj,
    }
    return render_to_response(template, template_dict, context_instance=RequestContext(request))