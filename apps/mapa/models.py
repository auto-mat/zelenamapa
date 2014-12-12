# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
from webmap.models import Poi
from webmap.utils import SlugifyFileSystemStorage


class SitPoi(models.Model):
    webmap_poi = models.OneToOneField(Poi)
    sit_geom = models.GeometryField(
        verbose_name=u"SIT poloha",
        srid=4326,
        blank=True,
        null=True,
        help_text=u"Původní poloha podle SITu",
        )


class Sit(models.Model):
    "Importovaná data ze SIT"
    webmap_poi = models.ForeignKey(Poi, null=True, blank=True)

    key = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        default="",
        verbose_name=u"key"
        )
    value = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        default="",
        verbose_name=u"value"
        )

UPRESNENI_CHOICE = (
    ('novy', u'Nový'),
    ('reseno', u'V řešení'),
    ('vyreseno', u'Vyřešeno'),
    ('zamitnuto', u'Zamítnuto'),
    )


class Upresneni(models.Model):
    """
    Tabulka pro uzivatelske doplnovani informaci do mapy.

    Prozatim na principu rucniho prepisu udaju v adminu.
    Vyzchazi z POI, ale nekopiruje se do ni.
    Slouzi predevsim k doplneni informace k mistu.
    Nektera pole mohou byt proto nefunkncni.
    """

    name = models.CharField(
        max_length=255,
        verbose_name="Název",
        )
    webmap_poi = models.ForeignKey(
        Poi,
        null=True,
        blank=True,
        )
    email = models.EmailField(
        verbose_name=u"Váš e-mail (pro další komunikaci)",
        null=True,
        )    # Prispevatel musi vyplnit email.
    status = models.CharField(
        max_length=10,
        choices=UPRESNENI_CHOICE,
        )
    desc = models.TextField(
        verbose_name=u"Popis (doplnění nebo oprava nebo popis nového místa, povinné pole)",
        null=True,
        )
    url = models.URLField(verbose_name=u"Odkaz, webové stránky místa (volitelné pole)",
                          null=True,
                          blank=True,
                          )  # Odkaz z vypisu - stranka podniku apod.
    address = models.CharField(
        verbose_name=u"Adresa místa, popis lokace (volitelné pole)",
        max_length=255,
        null=True,
        blank=True,
        )
    location = models.PointField(
        verbose_name=u"poloha",
        srid=4326,
        blank=True,
        null=True,
        help_text=u"Poloha přidávaného místa",
        )
    photo1 = models.ImageField(
        null=True,
        blank=True,
        upload_to='photo_upload',
        storage=SlugifyFileSystemStorage(),
        verbose_name="Foto 1",
        )
    photo2 = models.ImageField(
        null=True,
        blank=True,
        upload_to='photo_upload',
        storage=SlugifyFileSystemStorage(),
        verbose_name="Foto 2",
        )
    photo3 = models.ImageField(
        null=True,
        blank=True,
        upload_to='photo_upload',
        storage=SlugifyFileSystemStorage(),
        verbose_name="Foto 3",
        )
    created = models.DateTimeField(auto_now_add=True, verbose_name="created at")
    modified = models.DateTimeField(auto_now=True, verbose_name="last modification at")


    class Meta:
        verbose_name_plural = u"upřesnění"

    def __unicode__(self):
        return u"%s - %s" % (self.webmap_poi, self.email)


class Staticpage(models.Model):
    "Tabulka statickeho obsahu webu"
    slug = models.SlugField(
        unique=True,
        verbose_name="Slug",
        )  # extenze v URL
    head = models.TextField(
        verbose_name=u"Header section (additional css, js, etc.)",
        null=True,
        blank=True,
        )
    title = models.CharField(
        verbose_name=u"Titulek straky",
        max_length=255,
        null=True,
        blank=True,
        )
    short = models.TextField(
        verbose_name=u"Zkraceny html obsah (nahled)",
        null=True,
        )
    content = models.TextField(
        verbose_name=u"Html obsah",
        null=True,
        )

    def __unicode__(self):
        return self.title
