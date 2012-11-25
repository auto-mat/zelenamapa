# views.py

import random, math
import urllib, re

from django.conf import settings
from django import forms, http
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.gis.geos import Point
from django.contrib.gis.shortcuts import render_to_kml
from django.db.models import Max
from django.views.decorators.cache import cache_page
from django.views.decorators.cache import never_cache
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db.models import Q 

from mapa.models import *

def mapa_view(request, poi_id=None):
    vrstvy = Vrstva.objects.filter(status__show=True)
    vlastnosti = Vlastnost.objects.filter(status__show=True)

    # pro nahodny objekt v mape
    # tento kod selze pokud nemame v db zadne Poi
    random_poi = None
    try:
        max_id = Poi.objects.aggregate(Max('id')).values()[0]
        min_id = math.ceil(max_id*random.random())
        random_poi = Poi.viditelne.filter(id__gte=min_id).order_by('id')[0]
    except:
        pass

    # volitelne poi_id zadane mape jako bod, na ktery se ma zazoomovat
    center_poi = None
    if poi_id:
        try:
            center_poi = Poi.viditelne.get(id=poi_id)
        except Poi.DoesNotExist:
            pass

    # momentalne neni zapotrebi, ale ponechame si pro strycka prihodu
    titulni_stranka = request.get_full_path() == '/'

    # detekce mobilni verze podle url
    subdomain = request.META.get('HTTP_HOST', '').split('.')
    mobilni = False
    if 'm' in subdomain:
       mobilni = True

    context = RequestContext(request, {
        'vrstvy': vrstvy,
        'vlastnosti' : vlastnosti,
        'random_poi' : random_poi,
        'poi_count' : Poi.viditelne.count(),
        'center_poi' : center_poi,
        'titulni_stranka' : titulni_stranka,
        'mobilni' : mobilni,
    })
    return render_to_response('mapa.html', context_instance=context)

@never_cache              # zabranime prohlizeci cachovat si kml
@cache_page(24 * 60 * 60) # cachujeme view v memcached s platnosti 24h
def kml_view(request, nazev_vrstvy):
    # najdeme vrstvu podle slugu. pokud neexistuje, vyhodime 404
    v = get_object_or_404(Vrstva, slug=nazev_vrstvy, status__show=True)

    # vsechny body co jsou v teto vrstve a jsou zapnute
    points = Poi.viditelne.filter(znacka__vrstva=v).kml()
    return render_to_kml("gis/kml/vrstva.kml", { 'places' : points})

#@cache_page(24 * 60 * 60) # cachujeme view v memcached s platnosti 24h
def popup_view(request, poi_id):
    # najdeme vrstvu podle slugu. pokud neexistuje, vyhodime chybu
    poi = get_object_or_404(Poi, id=poi_id)

    return render_to_kml("gis/popup.html",
        context_instance=RequestContext(request, { 'poi' : poi }))

def search_view(request, query):
    if len(query) < 3:
        return http.HttpResponseBadRequest('Insufficient query lenght')
    ikona = None

    #  nejdriv podle nazvu
    nazev_qs = Poi.viditelne.filter(Q(nazev__icontains=query))
    # pak podle popisu, adresy a nazvu znacky, pokud uz nejsou vyse
    extra_qs = Poi.viditelne.filter(Q(desc__icontains=query)|Q(address__icontains=query)|Q(znacka__nazev__icontains=query)).exclude(id__in=nazev_qs)
    # union qs nezachova poradi, tak je prevedeme na listy a spojime
    points = list(nazev_qs.kml()) + list(extra_qs.kml())
    return render_to_kml("gis/kml/vrstva.kml", {
        'places' : points,
        'ikona': ikona})

# pro danou vrstvu vrati seznam bodu ve formatu txt
def txt_view(request, nazev_vrstvy):
    # najdeme vrstvu podle slugu. pokud neexistuje, vyhodime chybu
    v = Vrstva.objects.get(slug=nazev_vrstvy)
    # vsechny body co jsou v teto vrstve
    points = Poi.objects.filter(znacka__vrstva=v)
    return render_to_response('txtlayer.txt', { 'points': points})

class UpresneniForm(forms.ModelForm):
    class Meta:
        model = Upresneni
        fields = ('email', 'desc', 'url', 'address')

# View pro formular na uzivatelske vkladani oprav a doplnku
def addpoi_view(request, poi_id=None):
    static_vkladani = Staticpage.objects.get(slug='vkladani')
    if poi_id:
        poi = Poi.objects.get(id=poi_id)
        poi_desc = poi.nazev
    else:
        poi = None
        poi_desc = 'nove misto'

    if request.method == 'POST':
        obj = Upresneni(misto=poi, status='novy')
        form = UpresneniForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            # http://docs.djangoproject.com/en/dev/topics/email/
            from_email = 'form@zelenamapa.cz'
            to_email   = obj.email
            subject    = 'Doplneni Zelene mapy - ' + poi_desc
            message    = "Z Vaseho mailu (" + to_email + ") bylo zaslano doplneni Zelene mapy Prahy." + \
                         "Dekujeme za Vas prispevek!\n\n" +                                        \
                         "Obsah doplneni:\n" +                                                     \
                         "Misto         :"   + poi_desc + "\n" +                                   \
                         "Popis doplneni:\n" + obj.desc  + "\n\n" +                                \
                         "URL           :"   + obj.url  + "\n" +                                   \
                         "Adresa        :"   + obj.address  + "\n\n" +                             \
                         "Dekujeme za Vas doplnek, ozveme se vam po jeho vyhodnoceni\n\n" +        \
                         "V pripade nejasnosti nas kontaktujte na adrese doplneni@zelenamapa.cz .\n"
            # try:
            send_mail(subject, message, from_email, [to_email,'kontakt@zelenamapa.cz'])
            # except:
            #    return http.HttpResponse('Mail problem.')
        
            return http.HttpResponseRedirect(reverse(static_view, args=["dekujeme"]))
    else:
        form = UpresneniForm() # An unbound form

    return render_to_response('addpoi.html',
        context_instance=RequestContext(request, { 'poi': poi, 'form': form, 'static_vkladani' : static_vkladani }))

# View pro podrobny vypis mista
@cache_page(24 * 60 * 60) # cachujeme view v memcached s platnosti 24h
def detail_view(request, poi_id):
    poi = Poi.objects.get(id=poi_id)
    return render_to_response('misto.html',
        context_instance=RequestContext(request, { 'poi': poi }))

# View pro podrobny vypis seznamu vlastnosti
@cache_page(24 * 60 * 60) # cachujeme view v memcached s platnosti 24h
def vlastnosti_view(request):
    static_filtry = Staticpage.objects.get(slug='filtry')
    vlastnosti = Vlastnost.objects.filter(status__show='True')
    return render_to_response('vlastnosti.html',
        context_instance=RequestContext(request, { 'vlastnosti': vlastnosti, 'static_filtry' : static_filtry }))

# View pro podrobny vypis vrstev
@cache_page(24 * 60 * 60) # cachujeme view v memcached s platnosti 24h
def vrstvy_view(request):
    static_vrstvy = Staticpage.objects.get(slug='vrstvy')
    vrstvy = Vrstva.objects.filter(status__show=True)
    # vrstvy = Vrstva.objects.all()
    return render_to_response('vrstvy.html',
        context_instance=RequestContext(request, { 'vrstvy': vrstvy, 'static_vrstvy' : static_vrstvy }))
        
# View pro podrobny vypis znacek
@cache_page(24 * 60 * 60) # cachujeme view v memcached s platnosti 24h
def znacky_view(request):
    static_znacky = Staticpage.objects.get(slug='znacky')
    vrstvy = Vrstva.objects.filter(status__show=True)
    znacky = Znacka.objects.filter(status__show=True)
    return render_to_response('znacky.html',
        context_instance=RequestContext(request, { 'vrstvy': vrstvy, 'znacky': znacky, 'static_znacky' : static_znacky }))
        
# View pro podrobny vypis statickych objektu
@never_cache
@cache_page(24 * 60 * 60) # cachujeme view v memcached s platnosti 24h
def static_view(request, static_slug):
    static = get_object_or_404(Staticpage, slug=static_slug)
    return render_to_response('static.html',
        context_instance=RequestContext(request, { 'static': static }))

# View pro vypis ZMJ a jinych festivalu
@never_cache
def festival_view(request,akce_slug):
    # General settings (should be moved into DB based on akce_slug )
    vlastnost='zmj' # melo by se menit jinde, asi pres parametry ci nejak podobne...
    clanek   ='zmj'
    wp_incURL='' # "http://wp.zelenamapa.cz/?page_id=442" nefunguje, ma linky na jsfunkci a ne primo.
    wp_link  ='http://wp.zelenamapa.cz/?cat=8' 
    
    # integrace Wordpress kategorie
    wpcat = '';
    try:
        f = urllib.urlopen(wp_incURL)
        wpcat = f.read()
        f.close()
    except:
        pass
       
    pois_vlastnost = Poi.viditelne.filter(vlastnosti__slug=vlastnost)
    static_page = Staticpage.objects.get(slug=clanek)
        
    return render_to_response('festival.html',
        context_instance=RequestContext(request, { 
        'pois'         : pois_vlastnost,
        'wordpresscat' : wpcat,
        'wordpresslink': wp_link,
        'static'       : static_page
         }))
      
def m_hledani(request):
    vlastnosti = Vlastnost.objects.filter(status__show=True, filtr=True)
    return render_to_response('mobil/hledani.html',
        context_instance=RequestContext(request, {
                'vlastnosti': vlastnosti,
                }))
        
def m_vypis(request):
    qs = Poi.viditelne.all()
    vlastnosti = Vlastnost.objects.filter(status__show=True)
    for v in vlastnosti:
        if v.slug in request.GET:
            qs = qs.filter(vlastnosti_cache__icontains=v.slug)
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
        context_instance=RequestContext(request, { 'poi' : poi }))
