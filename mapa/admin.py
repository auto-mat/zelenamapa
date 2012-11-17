# admin.py

from django.conf import settings # needed if we use the GOOGLE_MAPS_API_KEY from settings

# Import the admin site reference from django.contrib.admin
from django.contrib import admin

# Grab the Admin Manager that automaticall initializes an OpenLayers map
# for any geometry field using the in Google Mercator projection with OpenStreetMap basedata
from django.contrib.gis.admin import OSMGeoAdmin

# Note, another simplier manager that does not reproject the data on OpenStreetMap is available
# with from `django.contrib.gis.admin import GeoModelAdmin`

# Finally, import our model from the working project
# the geographic_admin folder must be on your python path
# for this import to work correctly
from mapa.models import *

USE_GOOGLE_TERRAIN_TILES = False

class PoiAdmin(OSMGeoAdmin):
    list_display = ['nazev','status','znacka','address','url','foto_thumb']
    list_filter = ('znacka__vrstva', 'znacka', 'status',)
    exclude = ('vlastnosti_cache',)
    raw_id_fields = ('znacka',)
    search_fields = ('nazev',)
    ordering = ('nazev',)
    save_as = True
    search_fields = ['nazev']
    list_select_related = True
    filter_horizontal = ('vlastnosti',)

    if USE_GOOGLE_TERRAIN_TILES:
      map_template = 'gis/admin/google.html'
      extra_js = ['http://openstreetmap.org/openlayers/OpenStreetMap.js', 'http://maps.google.com/maps?file=api&amp;v=2&amp;key=%s' % settings.GOOGLE_MAPS_API_KEY]
    else:
      pass # defaults to OSMGeoAdmin presets of OpenStreetMap tiles

    # Default GeoDjango OpenLayers map options
    # Uncomment and modify as desired
    # To learn more about this jargon visit:
    # www.openlayers.org
    
    default_lon = 1605350
    default_lat = 6461466
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
    list_display = ('nazev', 'desc', 'vrstva', 'minzoom', 'status')
    search_fields = ('nazev', 'desc',)
    
class UpresneniAdmin(admin.ModelAdmin):
    model = Upresneni
    raw_id_fields = ('misto',)
    list_filter = ('status',)
    list_display = ('misto', 'email', 'status', 'desc',)

class StaticAdmin(admin.ModelAdmin):
    model = Staticpage
    
admin.site.register(Poi   , PoiAdmin   )
admin.site.register(Vrstva, VrstvaAdmin)
admin.site.register(Znacka, ZnackaAdmin)
admin.site.register(Status, admin.ModelAdmin)
admin.site.register(Vlastnost, VlastnostAdmin)
admin.site.register(Upresneni, UpresneniAdmin)
admin.site.register(Staticpage, StaticAdmin)
