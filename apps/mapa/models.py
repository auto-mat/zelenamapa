# -*- coding: utf-8 -*-
import datetime

from django.contrib.gis.db import models
from django.utils.safestring import mark_safe
from django.core.cache import cache

from django.contrib.auth.models import User

from .utils import SlugifyFileSystemStorage

class Status(models.Model):
    "Stavy zobrazeni konkretniho objektu, vrstvy apod."
    nazev   = models.CharField(max_length=255)                      # Nazev statutu
    desc    = models.TextField(null=True, blank=True)               # Description
    show    = models.BooleanField()                                 # Zobrazit uzivateli zvenci
    show_TU = models.BooleanField()                                 # Zobrazit editorovi mapy

    class Meta:
        verbose_name_plural = "Statuty"
    def __unicode__(self):
        return self.nazev
    

class Vrstva(models.Model):
    "Vrstvy, ktere se zobrazi v konkretni mape"
    nazev   = models.CharField(max_length=255)                      # Name of the layer
    slug    = models.SlugField(unique=True, verbose_name=u"název v URL")  # Vrstva v URL
    desc    = models.TextField(null=True, blank=True)               # Description
    status  = models.ForeignKey(Status)              # zobrazovaci status
    order   = models.PositiveIntegerField()
    remark  = models.TextField(null=True, blank=True, help_text=u"interni informace o objektu, ktere se nebudou zobrazovat")

    class Meta:
        verbose_name_plural = u"vrstvy"
        ordering = ['order']
    def __unicode__(self):
        return self.nazev

class Znacka(models.Model):
    "Mapove znacky vcetne definice zobrazeni"
    nazev   = models.CharField(max_length=255)   # Name of the mark
    
    # Relationships
    vrstva  = models.ForeignKey(Vrstva)              # Kazda znacka lezi prave v jedne vrstve
    status  = models.ForeignKey(Status)              # kvuli vypinani
    
    # icon: Neni zde, ale v tabulce znacky a vztahuje se k rozlicnym zobrazenim 
    # Pro zjednoduseni mame image "default_icon", ale to je jen nouzove reseni, 
    # ktere nesmi nahradit system znacek zavislych na zobrazeni, etc.
    
    # content 
    desc    = models.TextField(null=True, blank=True, help_text=u"podrobny popis znacky")
    remark  = models.TextField(null=True, blank=True, help_text=u"interni informace o objektu, ktere se nebudou zobrazovat")
    
    # Base icon and zoom dependent display range
    default_icon = models.ImageField(null=True, upload_to='ikony', storage=SlugifyFileSystemStorage()) # XXX: zrusit null=True
    mobile_icon = models.ImageField(null=True, upload_to='ikony_m', storage=SlugifyFileSystemStorage()) # XXX: zrusit null=True
    minzoom = models.PositiveIntegerField(default=1)
    maxzoom = models.PositiveIntegerField(default=10)
    
    class Meta:
        verbose_name_plural = "Znacky"
    def __unicode__(self):
        return self.nazev

class ViditelneManager(models.GeoManager):
    def get_query_set(self):
        return super(ViditelneManager, self).get_query_set().filter(status__show=True, znacka__status__show=True)

class Poi(models.Model):
    "Misto - bod v mape"
    author = models.ForeignKey(User, verbose_name="Autor")
    created_at = models.DateTimeField(auto_now_add=True,  verbose_name="Posledni zmena")

    nazev   = models.CharField(max_length=255, verbose_name=u"název")   # Name of the location
    
    # Relationships
    znacka  = models.ForeignKey(Znacka, verbose_name=u"značka")          # "Znacky"   - misto ma prave jednu
    status  = models.ForeignKey(Status)          # "Statuty"  - misto ma prave jeden
    vlastnosti    = models.ManyToManyField('Vlastnost', blank=True, null=True)       # "Vlastnosti" - ma vice
    
    # "dulezitost" - modifikator minimalniho zoomu, ve kterem se misto zobrazuje. 
    dulezitost = models.SmallIntegerField(default=0, verbose_name=u"důležitost",
                 help_text=u"""Modifikátor minimalniho zoomu, ve kterém se místo zobrazuje (20+ bude vidět vždy). 
                               Cíl je mít výběr základních objektů viditelných ve velkých měřítcích
                               a zabránit přetížení mapy značkami v přehledce.
                               Lze použít pro placenou reklamu! ("Váš podnik bude vidět hned po otevření mapy")""")
    
    # Geographical intepretation
    geom    = models.GeometryField(verbose_name=u"poloha",srid=4326, help_text=u"Klikni na tužku s plusem a umisti bod na mapu")
    objects = models.GeoManager()
    
    # Own content (facultative)
    desc    = models.TextField(null=True, blank=True, verbose_name=u"popis", help_text=u"Text do buliny na mapě")
    desc_extra = models.TextField(null=True, blank=True, verbose_name=u"podrobný popis", help_text="Text do detailu místa (mimo bublinu)")
    url     = models.URLField(null=True, blank=True, help_text=u"Webový odkaz na stránku podniku apod.")
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name=u"adresa")
    remark  = models.TextField(null=True, blank=True, verbose_name=u"interní poznámka", help_text=u"Interní informace o objektu, které se nebudou zobrazovat")

    # 3 fotografie museji pro vetsinu ucelu stacit
    foto_thumb  = models.ImageField(null=True, blank=True,
                                    upload_to='foto', storage=SlugifyFileSystemStorage(),
                                    verbose_name=u"foto",
                                    help_text=u"velikost max. 500x400px")
#    foto2 = models.ImageField(null=True, blank=True, upload_to='foto') 
#    foto3 = models.ImageField(null=True, blank=True, upload_to='foto') 
    
    # zde se ulozi slugy vsech vlastnosti, aby se pri renederovani kml
    # nemusel delat db dotaz pro kazde Poi na jeho vlastnosti
    vlastnosti_cache = models.CharField(max_length=255, null=True, blank=True)
    
    viditelne = ViditelneManager()
    
    class Meta:
        verbose_name = "místo"
        verbose_name_plural = "místa"
    def __unicode__(self):
        return self.nazev
    def save_vlastnosti_cache(self):
        self.vlastnosti_cache = u",".join([v.slug for v in self.vlastnosti.filter(status__show=True)])
        self.save()
    def get_absolute_url(self):
        return "/misto/%i/" % self.id

    def save(self, *args, **kwargs):
        self.created_at = datetime.datetime.now()
        super(Poi, self).save(*args, **kwargs)

class Sit(models.Model):
    "Importovaná data ze SIT"
    poi = models.OneToOneField(Poi, related_name="sit")

    sit_id = models.IntegerField(default=0, unique=True)
    sit_id_um = models.CharField(max_length=255, null=True, blank=True, verbose_name=u"id_um")
    sit_znaceni = models.CharField(max_length=255, null=True, blank=True, verbose_name=u"id_znaceni")
    sit_rc = models.CharField(max_length=255, null=True, blank=True, verbose_name=u"rc")
    sit_lokalita = models.CharField(max_length=255, null=True, blank=True, verbose_name=u"lokalita")

from django.db.models.signals import m2m_changed, post_save
def update_vlastnosti_cache(sender, instance, action, reverse, model, pk_set, **kwargs):
    "Aktualizace cache vlastnosti pri ulozeni Poi. Je treba jeste vyresit smazani Vlastnosti"
    if action == 'post_add':
        instance.save_vlastnosti_cache()
m2m_changed.connect(update_vlastnosti_cache, Poi.vlastnosti.through) 

def invalidate_cache(sender, instance, **kwargs):
    if sender in [Status, Vrstva, Znacka, Poi, Vlastnost, Staticpage]:
        cache.clear()
post_save.connect(invalidate_cache)

class Sektor(models.Model):
    "Sektor mapy"
    nazev   = models.CharField(max_length=255)
    slug    = models.SlugField(unique=True, verbose_name="Slug")
    
    geom    = models.PolygonField(verbose_name=u"plocha",srid=4326, help_text=u"Plocha sektoru")
    objects = models.GeoManager()

class Vlastnost(models.Model):
    "Vlastnosti mist"
    nazev   = models.CharField(max_length=255)   # Name of the property
    status  = models.ForeignKey(Status)          # "Statuty"  - tj. active/inactive. Mozny je i boolean "active"
    filtr   = models.BooleanField()              # Pouzit v levem menu, filtrovat???
    poradi  = models.PositiveIntegerField()
    # content 
    slug    = models.SlugField(unique=True, verbose_name="Slug")  # Popis tagu v URL
    desc    = models.TextField(null=True, blank=True) # podrobny popis vlastnosti
    remark  = models.TextField(null=True, blank=True, help_text=u"interni informace o objektu, ktere se nebudou zobrazovat")
    default_icon = models.ImageField(null=True, upload_to='ikony', storage=SlugifyFileSystemStorage()) # XXX: zrusit null=True
   
    class Meta:
        verbose_name_plural = u"vlastnosti"
	ordering = ['poradi']
    def __unicode__(self):
        return self.nazev

UPRESNENI_CHOICE = (
        ('novy', u'Nový'),
        ('reseno', u'V řešení'),
        ('vyreseno', u'Vyřešeno'),
        ('zamitnuto', u'Zamítnuto'),
)

class Upresneni(models.Model):
    """
    Tabulka pro uzivatelske doplnovani informaci do mapy. 
    Prozatim na proncipu rucniho prepisu udaju v adminu.
    Vyzchazi z POI, ale nekopiruje se do ni.
    Slouzi predevsim k doplneni informace k mistu. Nektera pole mohou byt proto nefunkncni.
    """
    misto  = models.ForeignKey(Poi, blank=True, null=True) # Odkaz na objekt, ktery chce opravit, muze byt prazdne.
    email  = models.EmailField(verbose_name=u"Váš e-mail (pro další komunikaci)", null=True)    # Prispevatel musi vyplnit email.
    status  = models.CharField(max_length=10,choices=UPRESNENI_CHOICE) 
    desc    = models.TextField(verbose_name=u"Popis (doplnění nebo oprava nebo popis nového místa, povinné pole)",null=True)
    url     = models.URLField(verbose_name=u"Odkaz, webové stránky místa (volitelné pole)",null=True, blank=True)  # Odkaz z vypisu - stranka podniku apod.
    address = models.CharField(verbose_name=u"Adresa místa, popis lokace (volitelné pole)",max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = u"upřesnění"
    def __unicode__(self):
        return u"%s - %s" % (self.misto, self.email)

    
class Staticpage(models.Model):
    "Tabulka statickeho obsahu webu"
    slug    = models.SlugField(unique=True, verbose_name="Slug")  # extenze v URL
    head    = models.TextField(verbose_name=u"Header section (additional css, js, etc.)",null=True, blank=True)
    title   = models.CharField(verbose_name=u"Titulek straky",max_length=255, null=True, blank=True)
    short   = models.TextField(verbose_name=u"Zkraceny html obsah (nahled)",null=True)
    content = models.TextField(verbose_name=u"Html obsah",null=True)
    
    def __unicode__(self):
        return self.title
