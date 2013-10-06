# -*- coding: utf-8 -*-
# admin.py

from django.conf import settings # needed if we use the GOOGLE_MAPS_API_KEY from settings

# Import the admin site reference from django.contrib.admin
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.auth.admin import UserAdmin
from constance import config
import fgp

# Grab the Admin Manager that automaticall initializes an OpenLayers map
# for any geometry field using the in Google Mercator projection with OpenStreetMap basedata
from django.contrib.gis.admin import OSMGeoAdmin
from django.contrib.gis.geos import Point

# Note, another simplier manager that does not reproject the data on OpenStreetMap is available
# with from `django.contrib.gis.admin import GeoModelAdmin`

# Finally, import our model from the working project
# the geographic_admin folder must be on your python path
# for this import to work correctly
from mapa.models import *

USE_GOOGLE_TERRAIN_TILES = False

class UserAdmin(UserAdmin):
    list_display = ('__unicode__', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active', 'last_login', 'get_groups', 'get_user_permissions')

    def get_groups(self, obj):
        if obj:
            return ", ".join([group.name for group in obj.groups.all()])

    def get_user_permissions(self, obj):
        if obj:
            return ", ".join([user_permission.name for user_permission in obj.user_permissions.all()])


class SektorFilter(SimpleListFilter):
    title = (u"Sektor")
    parameter_name = u"sektor"

    def lookups(self, request, model_admin):
        return [("mimo", u"Mimo sektory")] + [(sektor.slug, sektor.nazev) for sektor in Sektor.objects.all()]

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        if self.value() == "mimo":
            for sektor in Sektor.objects.all():
                queryset = queryset.exclude(geom__contained = sektor.geom)
            return queryset
        return queryset.filter(geom__contained = Sektor.objects.get(slug = self.value()).geom)

class SitInline(admin.TabularInline):
    model = Sit
    readonly_fields = ("key", "value")
    extra = 0
    can_delete = False

@fgp.enforce
class PoiAdmin(OSMGeoAdmin):
    model = Poi
    list_display = ['nazev','status','znacka','address','url','foto_thumb', 'desc' ]
    list_filter = (SektorFilter, 'znacka__vrstva', 'znacka', 'status',)
    exclude = ('vlastnosti_cache', )
    readonly_fields = ("created_at", "author", "sit_geom")
    raw_id_fields_readonly = ('znacka',)
    search_fields = ('nazev',)
    ordering = ('nazev',)
    save_as = True
    search_fields = ['nazev']
    list_select_related = True
    filter_horizontal = ('vlastnosti',)
    list_max_show_all = 10000
    inlines = [ SitInline, ]

    if USE_GOOGLE_TERRAIN_TILES:
      map_template = 'gis/admin/google.html'
      extra_js = ['http://openstreetmap.org/openlayers/OpenStreetMap.js', 'http://maps.google.com/maps?file=api&amp;v=2&amp;key=%s' % settings.GOOGLE_MAPS_API_KEY]
    else:
      pass # defaults to OSMGeoAdmin presets of OpenStreetMap tiles

    # Default GeoDjango OpenLayers map options
    # Uncomment and modify as desired
    # To learn more about this jargon visit:
    # www.openlayers.org
    
    def get_form(self, request, obj=None, **kwargs):
         pnt = Point(config.MAP_BASELON, config.MAP_BASELAT, srid=4326)
         pnt.transform(900913)
         self.default_lon, self.default_lat = pnt.coords

         if request.user.has_perm(u'mapa.can_only_own_data_only') and obj and obj.author != request.user:
             self.fields = ('nazev', )
             self.readonly_fields = ('nazev', )
         else:
             self.fields = PoiAdmin.fields
             self.readonly_fields = PoiAdmin.readonly_fields
         return super(PoiAdmin, self).get_form(request, obj, **kwargs)

    default_zoom = 12
    #display_wkt = False
    #display_srid = False
    #extra_js = []
    #num_zoom = 18
    #max_zoom = False
    #min_zoom = False
    #units = False
    #max_resolution = False
    #max_extent = False
    #modifiable = True
    #mouse_position = True
    #scale_text = True
    #layerswitcher = True
    scrollable = False
    #admin_media_prefix = settings.ADMIN_MEDIA_PREFIX
    map_width = 700
    map_height = 500
    map_srid = 900913
    #map_template = 'gis/admin/openlayers.html'
    #openlayers_url = 'http://openlayers.org/api/2.6/OpenLayers.js'
    #wms_url = 'http://labs.metacarta.com/wms/vmap0'
    #wms_layer = 'basic'
    #wms_name = 'OpenLayers WMS'
    #debug = False
    #widget = OpenLayersWidget

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user # no need to check for it.
        obj.save()

class SektorAdmin(OSMGeoAdmin):
    list_display = ('nazev',)
    prepopulated_fields = {'slug': ('nazev',) } # slug se automaticky vytvari z nazvu
    if USE_GOOGLE_TERRAIN_TILES:
      map_template = 'gis/admin/google.html'
      extra_js = ['http://openstreetmap.org/openlayers/OpenStreetMap.js', 'http://maps.google.com/maps?file=api&amp;v=2&amp;key=%s' % settings.GOOGLE_MAPS_API_KEY]
    else:
      pass # defaults to OSMGeoAdmin presets of OpenStreetMap tiles

    def get_form(self, request, obj=None, **kwargs):
         pnt = Point(config.MAP_BASELON, config.MAP_BASELAT, srid=4326)
         pnt.transform(900913)
         self.default_lon, self.default_lat = pnt.coords
         return super(SektorAdmin, self).get_form(request, obj, **kwargs)

    default_zoom = 12
    scrollable = False
    map_width = 700
    map_height = 500
    map_srid = 900913

class ZnackaInline(admin.TabularInline):
    model = Znacka

class VrstvaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nazev',) } # slug se automaticky vytvari z nazvu
    list_display = ['nazev', 'status', 'order']
    inlines = [ZnackaInline]

class MapaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nazev',) } # slug se automaticky vytvari z nazvu

class VlastnostAdmin(admin.ModelAdmin):
    list_display = ('nazev', 'filtr', 'status')
    model = Vlastnost

class ZnackaAdmin(admin.ModelAdmin):
    list_display = ('nazev', 'desc', 'vrstva', 'minzoom', 'status', 'default_icon_image')
    search_fields = ('nazev', 'desc',)

    def default_icon_image(self, obj):
        if obj.default_icon:
            return '<img src="%s"/>' % obj.default_icon.url
    default_icon_image.allow_tags = True

    def get_form(self, request, obj=None, **kwargs):
        if request.user.has_perm(u'mapa.can_only_view'):
            self.fields = ('nazev', )
            self.readonly_fields = ('nazev', )
        return super(ZnackaAdmin, self).get_form(request, obj, **kwargs)

class StatusAdmin(admin.ModelAdmin):
    list_display = ('nazev', 'desc', 'show', 'show_TU')
    
class UpresneniAdmin(admin.ModelAdmin):
    model = Upresneni
    raw_id_fields = ('misto',)
    list_filter = ('status',)
    list_display = ('misto', 'email', 'status', 'desc',)

class StaticAdmin(admin.ModelAdmin):
    model = Staticpage
    
admin.site.register(Poi   , PoiAdmin   )
admin.site.register(Vrstva, VrstvaAdmin)
admin.site.register(Sektor, SektorAdmin)
admin.site.register(Znacka, ZnackaAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Vlastnost, VlastnostAdmin)
admin.site.register(Upresneni, UpresneniAdmin)
admin.site.register(Staticpage, StaticAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
