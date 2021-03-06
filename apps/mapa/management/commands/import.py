from django.core.management.base import BaseCommand, make_option
from django.contrib.gis.utils import LayerMapping
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.db import models
from mapa.models import Poi, Znacka, Status, Sit
from django.contrib.auth.models import User

znacka_id = 0
status_id = 0
author_id = 0
import_fields = []
table_name = ""

# Helper object to transfor imported data
class ImportPoi(Poi):
    sit_id = models.IntegerField(default=0)
    sit_id_um = models.CharField(max_length=255, null=True, blank=True, verbose_name=u"id_um")
    sit_ssz_id = models.IntegerField(default=0)
    sit_znaceni = models.CharField(max_length=255, null=True, blank=True, verbose_name=u"id_znaceni")
    sit_rc = models.CharField(max_length=255, null=True, blank=True, verbose_name=u"rc")
    sit_lokalita = models.CharField(max_length=255, null=True, blank=True, verbose_name=u"lokalita")
    sit_prvek = models.CharField(max_length=255, null=True, blank=True, verbose_name=u"prvek")
    sit_oblast = models.CharField(max_length=255, null=True, blank=True)
    sit_typ = models.CharField(max_length=255, null=True, blank=True)
    sit_typ_stan = models.CharField(max_length=255, null=True, blank=True)
    sit_organizace = models.CharField(max_length=255, null=True, blank=True)
    sit_provozovat = models.CharField(max_length=255, null=True, blank=True)
    sit_cc_typ = models.CharField(max_length=255, null=True, blank=True)
    sit_poznamka = models.CharField(max_length=255, null=True, blank=True)
    sit_drevina = models.CharField(max_length=255, null=True, blank=True)
    sit_adresa = models.CharField(max_length=255, null=True, blank=True)
    sit_kod_co = models.IntegerField(default=0)
    sit_kod_mc = models.IntegerField(default=0)
    sit_katastr = models.IntegerField(default=0)
    sit_id_hriste = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        poi = Poi()
        poi.znacka = Znacka.objects.get(pk = znacka_id)
        poi.status = Status.objects.get(pk = status_id)
        poi.author = User.objects.get(pk = author_id)
        if self.nazev or self.nazev != "":
            poi.nazev = self.nazev
        else:
            poi.nazev = "%s - %s" % (self.sit_rc, self.desc)

        if poi.nazev == "":
            poi.nazev = "SIT import"

        #Just to be shown in output
        self.nazev = poi.nazev

        poi.desc = self.desc
        poi.geom = self.geom
        poi.sit_geom = self.geom
        poi.save()

        Sit(key = 'table_name', value = table_name, poi = poi).save()
        for field in import_fields:
            if field == 'popis':
                Sit(key = field, value = self.desc, poi = poi).save()
                continue
            if field == 'nazev':
                Sit(key = field, value = self.nazev, poi = poi).save()
                continue
            Sit(key = field, value = getattr(self, 'sit_' + field), poi = poi).save()

class Command(BaseCommand):
    help = "Import data from SIT"

    option_list = BaseCommand.option_list + (
        make_option('--znacka',
            action='store',
            dest='znacka_id',
            default=0,
            help='Set znacka id for new Poi objects'),
        make_option('--status',
            action='store',
            dest='status_id',
            default=0,
            help='Set status id for new Poi objects'),
        make_option('--author',
            action='store',
            dest='author_id',
            default=0,
            help='Set author id for new Poi objects'),
        )

    def print_layer_info(self, ds):
        layer = ds[0]
        print "Table name: %s" % layer.name
        print "Fields: %s" % layer.fields
        print "Features in layer: %s" % len(layer)
        print "Geom type: %s" % layer.geom_type
        print "WGS84 in WKT: %s" % layer.srs

    def handle(self, *args, **options):
        global znacka_id, status_id, author_id, import_fields, table_name
        znacka_id = options['znacka_id']
        status_id = options['status_id']
        author_id = options['author_id']
        data_source = DataSource(args[0])
        self.print_layer_info(data_source)
        fields = data_source[0].fields
        geom_type = data_source[0].geom_type
        table_name = data_source[0].name

        if geom_type == 'Point':
            mapping = {
                       'geom' : 'POINT',
                      }
    
        if geom_type == "LineString":
            mapping = {
                       'geom' : 'LINESTRING',
                      }
        
        if geom_type == "Polygon":
            mapping = {
                       'geom' : 'POLYGON',
                      }

        for field in fields:
            if field == 'popis':
                mapping['desc'] = 'popis'
                continue
            if field == 'nazev':
                mapping['nazev'] = 'nazev'
                continue
            mapping['sit_' + field] = field

        import_fields = fields

        source_srs = "+proj=krovak +lat_0=49.5 +lon_0=24.83333333333333 +alpha=30.28813972222222 \
                +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +pm=greenwich +units=m +no_defs \
                +towgs84=570.8,85.7,462.8,4.998,1.587,5.261,3.56"
        encoding = "WINDOWS-1250"
        lm = LayerMapping(ImportPoi, args[0], mapping, source_srs = source_srs, encoding = encoding)
        lm.save(verbose=True)
