# -*- coding: utf-8 -*-
# views.py

import random
import math
import urllib

from django import forms, http
from django.contrib.gis.forms import OSMWidget, PointField
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.gis.geos import Point
from django.contrib.gis.shortcuts import render_to_kml
from django.contrib.sites.models import get_current_site
from django.db.models import Max
from django.views.decorators.cache import cache_page
from django.views.decorators.cache import never_cache
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db.models import Q, Count

from mapa.models import Upresneni, Staticpage
from webmap.models import Poi, Layer, Property, Photo, Marker, Legend

from constance import config


def is_mobilni(request):
    subdomain = request.META.get('HTTP_HOST', '').split('.')
    try:
        request.GET["m"]
        explicit_mobile = True
    except KeyError:
        explicit_mobile = False
    return ('m' in subdomain) or (explicit_mobile)

def get_znacky():
    znacky = Marker.objects.filter(status__show=True, layer__status__show=True)
    for znacka in znacky:
        znacka.vlastnosti = Property.objects.filter(status__show=True).all()
        for vlastnost in znacka.vlastnosti:
            vlastnost.poi_count = vlastnost.poi_set.filter(marker = znacka, status__show=True).count()
        znacka.vlastnosti = sorted(znacka.vlastnosti, key = lambda a: a.poi_count, reverse = True)
        znacka.vlastnosti = filter(lambda a: a.poi_count != 0, znacka.vlastnosti)
    return znacky

def mapa_view(request, poi_id=None, template_name='mapa.html'):
    vrstvy = Layer.objects.filter(status__show=True)

    select_poi = None
    select_poi_header = 'Zajimave misto'  # jak s diaktritikou???
    if config.ENABLE_FEATURE_LEFT_POI_TIP:
        # prvni misto, ktere ma vlastnost se slugem "misto-mesice"
        select_poi_header = Property.objects.get(slug='misto-mesice').name
        try:
            select_poi = Poi.visible.filter(
                properties__slug='misto-mesice').order_by('id')[0]
        except:
            pass
    else:
        # pro nahodny objekt v mape
        # tento kod selze pokud nemame v db zadne Poi
        try:
            max_id = Poi.objects.aggregate(Max('id')).values()[0]
            min_id = math.ceil(max_id*random.random())
            select_poi = Poi.visible.filter(id__gte=min_id).order_by('id')[0]
        except:
            pass

    select2_pois = None
    select2_pois_header = 'Tipy:'  # jak s diaktritikou???
    # vybrana mista pro druhy vypis - kolik jich je, tolik jich je!
    try:
        select2_pois_header = Property.objects.get(slug='misto-propagace').name
        select2_pois = Poi.visible.filter(vlastnosti__slug='misto-propagace')
    except:
        pass

    # volitelne poi_id zadane mape jako bod, na ktery se ma zazoomovat
    center_poi = None
    if poi_id:
        try:
            center_poi = Poi.visible.get(id=poi_id)
        except Poi.DoesNotExist:
            pass

    # momentalne neni zapotrebi, ale ponechame si pro strycka prihodu
    titulni_stranka = request.get_full_path() == '/'

    # detekce mobilni verze podle url
    mobilni = is_mobilni(request)

    context = RequestContext(request, {
        'vrstvy': vrstvy,
        'znacky': get_znacky,
        'select_poi': select_poi,
        'select2_pois': select2_pois,
        'legenda': Legend.objects.all(),
        'poi_count': Poi.visible.count(),
        'center_poi': center_poi,
        'titulni_stranka': titulni_stranka,
        'mobilni': mobilni,
        'config': config,
        'site': get_current_site(request).domain,
        'select_poi_header': select_poi_header,
        'select2_pois_header': select2_pois_header,
        'static_filtry': Staticpage.objects.get(slug='filtry'),
        'static_ostatni_projekty': Staticpage.objects.get(slug='ostatni_projekty'),
        'vlastnosti': Property.objects.filter(status__show='True')
    })
    return render_to_response(template_name, context_instance=context)


#@cache_page(24 * 60 * 60) # cachujeme view v memcached s platnosti 24h
def popup_view(request, poi_id):
    # najdeme vrstvu podle slugu. pokud neexistuje, vyhodime chybu
    poi = get_object_or_404(Poi, id=poi_id)

    return render_to_kml("gis/popup.html",
                         context_instance=RequestContext(request, {
                             'poi': poi,
                             'fotky': poi.photos.all(),
                             'site': get_current_site(request).domain,
                             }))


# pro danou vrstvu vrati seznam bodu ve formatu txt
def txt_view(request, name_vrstvy):
    # najdeme vrstvu podle slugu. pokud neexistuje, vyhodime chybu
    v = Layer.objects.get(slug=name_vrstvy)
    # vsechny body co jsou v teto vrstve
    points = Poi.objects.filter(znacka__vrstva=v)
    return render_to_response('txtlayer.txt', {'points': points})


class UpresneniForm(forms.ModelForm):
    location = PointField(
        label=u"Poloha místa",
        required=False,
        )

    class Meta:
        model = Upresneni
        fields = ('name', 'desc', 'location', 'address', 'url', 'email', 'photo1', 'photo2', 'photo3')

    def __init__(self, *args, **kwargs):
        poi_id = kwargs.pop('poi_id')
        super(UpresneniForm, self).__init__(*args, **kwargs)

        self.fields['location'].widget=OSMWidget(attrs={
            'geom_type': 'POINT',
            'default_lat': config.MAP_BASELAT,
            'default_lon': config.MAP_BASELON,
            'default_zoom': 14,
        })
        self.fields['location'].widget.template_name = "gis/openlayers-osm-custom.html"

        if poi_id:
            for field in {'name', 'location', 'address', 'url'}:
                self.fields.pop(field)


# View pro formular na uzivatelske vkladani oprav a doplnku
def addpoi_view(request, poi_id=None):
    static_vkladani = Staticpage.objects.get(slug='vkladani')
    if poi_id:
        poi = Poi.objects.get(id=poi_id)
        poi_desc = poi.name
    else:
        poi = None
        poi_desc = 'nove misto'

    if request.method == 'POST':
        obj = Upresneni(webmap_poi=poi, status='novy')
        form = UpresneniForm(request.POST, instance=obj, poi_id=poi_id)
        if form.is_valid():
            form.save()
            # http://docs.djangoproject.com/en/dev/topics/email/
            from_email = 'form@zelenamapa.cz'
            to_email = obj.email
            subject = u'Doplnění Zelené mapy - ' + poi_desc
            message = u"Z Vašeho emailu (" + to_email + u") bylo zasláno doplnění Zelené mapy Prahy." + \
                      u"Děkujeme za Váš příspěvek!\n\n" +                                        \
                      u"Obsah doplnění:\n"
            if obj.name:
                message += u"Název         :" + obj.name + "\n"
            message += u"Místo         :" + poi_desc + "\n"
            if obj.location:
                message += u"Umístění      :" + str(obj.location) + "\n\n"
            if obj.desc:
                message += u"Popis doplnění:" + obj.desc + "\n\n"
            if obj.url:
                message += u"URL           :" + obj.url + "\n"
            if obj.address:
                message += u"Adresa        :" + obj.address + "\n\n"
            if obj.photo1:
                message += u"Fotografie 1  :" + obj.photo1.url + "\n\n"
            if obj.photo2:
                message += u"Fotografie 2  :" + obj.photo2.url + "\n\n"
            if obj.photo3:
                message += u"Fotografie 3  :" + obj.photo3.url + "\n\n"
            message += u"Děkujeme za Váš doplněk, ozveme se vám po jeho vyhodnocení\n\n" \
                       u"V případě nejasností nás kontaktujte na adrese doplneni@plzne.cz .\n"

            # try:
            send_mail(subject, message, from_email, [to_email, 'kontakt@plzne.cz'])
            # except:
            #    return http.HttpResponse('Mail problem.')

            return http.HttpResponseRedirect(reverse(static_view, args=["dekujeme"]))
    else:
        form = UpresneniForm(poi_id=poi_id)  # An unbound form

    return render_to_response('addpoi.html',
                              context_instance=RequestContext(request, {
                                  'poi': poi,
                                  'form': form,
                                  'static_vkladani': static_vkladani
                                  }))


# View pro podrobny vypis mista
@cache_page(24 * 60 * 60)  # cachujeme view v memcached s platnosti 24h
def detail_view(request, poi_id):
    poi = Poi.objects.get(id=poi_id)
    return render_to_response('misto.html',
                              context_instance=RequestContext(request, {
                                  'poi': poi,
                                  'fotky': Photo.objects.filter(poi=poi).order_by('order'),
                                  'config': config,
                                  'site': get_current_site(request).domain,
                                  }))


# View pro podrobny vypis seznamu vlastnosti
@cache_page(24 * 60 * 60)  # cachujeme view v memcached s platnosti 24h
def vlastnosti_view(request):
    static_filtry = Staticpage.objects.get(slug='filtry')
    vlastnosti = Property.objects.filter(status__show='True')
    return render_to_response('vlastnosti.html',
                              context_instance=RequestContext(request, {
                                  'vlastnosti': vlastnosti,
                                  'static_filtry': static_filtry
                                  }))


# View pro podrobny vypis vrstev
@cache_page(24 * 60 * 60)  # cachujeme view v memcached s platnosti 24h
def vrstvy_view(request):
    static_vrstvy = Staticpage.objects.get(slug='vrstvy')
    vrstvy = Layer.objects.filter(status__show=True)
    # vrstvy = Layer.objects.all()
    return render_to_response('vrstvy.html',
                              context_instance=RequestContext(request, {
                                  'vrstvy': vrstvy,
                                  'static_vrstvy': static_vrstvy
                                  }))


# View pro podrobny vypis znacek
@cache_page(24 * 60 * 60)  # cachujeme view v memcached s platnosti 24h
def znacky_view(request):
    static_znacky = Staticpage.objects.get(slug='znacky')
    vrstvy = Layer.objects.filter(status__show=True)
    znacky = Marker.objects.filter(status__show=True)
    return render_to_response('znacky.html',
                              context_instance=RequestContext(request, {
                                  'vrstvy': vrstvy,
                                  'znacky': znacky,
                                  'static_znacky': static_znacky
                                  }))


# View pro podrobny vypis statickych objektu
@never_cache
@cache_page(24 * 60 * 60)  # cachujeme view v memcached s platnosti 24h
def static_view(request, static_slug):
    static = get_object_or_404(Staticpage, slug=static_slug)
    return render_to_response('static.html',
                              context_instance=RequestContext(request, {'static': static}))


# View pro vypis ZMJ a jinych festivalu
@never_cache
def festival_view(request, akce_slug):
    # General settings (should be moved into DB based on akce_slug )
    vlastnost = 'zmj'  # melo by se menit jinde, asi pres parametry ci nejak podobne...
    clanek = 'zmj'
    wp_incURL = ''  # "http://wp.zelenamapa.cz/?page_id=442" nefunguje, ma linky na jsfunkci a ne primo.
    wp_link = 'http://wp.zelenamapa.cz/?cat=8'

    # integrace Wordpress kategorie
    wpcat = ''
    try:
        f = urllib.urlopen(wp_incURL)
        wpcat = f.read()
        f.close()
    except:
        pass

    pois_vlastnost = Poi.visible.filter(vlastnosti__slug=vlastnost)
    static_page = Staticpage.objects.get(slug=clanek)

    return render_to_response('festival.html',
                              context_instance=RequestContext(request, {
                                  'pois': pois_vlastnost,
                                  'wordpresscat': wpcat,
                                  'wordpresslink': wp_link,
                                  'static': static_page
                                  }))


def m_hledani(request):
    vlastnosti = Property.objects.filter(status__show=True, as_filter=True)
    return render_to_response('mobil/hledani.html',
                              context_instance=RequestContext(request, {
                                  'vlastnosti': vlastnosti,
                                  }))


def m_vypis(request):
    qs = Poi.visible.all()
    vlastnosti = Property.objects.filter(status__show=True)
    for v in vlastnosti:
        if v.slug in request.GET:
            qs = qs.filter(properties_cache__icontains=v.slug)
    lon = request.GET.get('lon', None)
    lat = request.GET.get('lat', None)
    if lon and lat:
        poloha = Point(float(lon), float(lat))
        qs = qs.distance(poloha).order_by('distance')
    return render_to_response('mobil/vypis.html',
                              context_instance=RequestContext(request, {
                                  'pois': qs[0:100]
                                  }))


def m_detail(request, poi_id):
    # najdeme vrstvu podle slugu. pokud neexistuje, vyhodime chybu
    poi = get_object_or_404(Poi, id=poi_id)

    return render_to_response("mobil/detail.html",
                              context_instance=RequestContext(request, {
                                  'poi': poi,
                                  'fotky': Photo.objects.filter(poi=poi).order_by('order'),
                              }))
