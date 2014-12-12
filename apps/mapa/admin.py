# -*- coding: utf-8 -*-
# admin.py

# Import the admin site reference from django.contrib.admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from webmap.models import Poi, Marker, Photo, License
import webmap
from django.contrib.auth.models import User
from mapa.models import Upresneni, Staticpage, Sit, SitPoi
from django.contrib.gis.admin import OSMGeoAdmin
from django.utils.html import mark_safe


class UserAdmin(UserAdmin):
    list_display = (
        '__unicode__', 'email', 'first_name', 'last_name', 'is_staff',
        'is_superuser', 'is_active', 'last_login', 'get_groups',
        'get_user_permissions')

    def get_groups(self, obj):
        if obj:
            return ", ".join([group.name for group in obj.groups.all()])

    def get_user_permissions(self, obj):
        if obj:
            return ", ".join([
                user_permission.name
                for user_permission in obj.user_permissions.all()
                ])


class SitPoiInline(admin.TabularInline):
    model = SitPoi
    readonly_fields = ("sit_geom",)
    extra = 0
    can_delete = False


class SitInline(admin.TabularInline):
    model = Sit
    readonly_fields = ("key", "value")
    extra = 0
    can_delete = False


class Webmap_PoiAdmin(webmap.admin.PoiAdmin):
    inlines = webmap.admin.PoiAdmin.inlines + [SitPoiInline, SitInline, ]

def make_photo(photo_field, email, poi):
    if photo_field:
        photo = Photo(
                photo=photo_field,
                photographer=email,
                license=License.objects.get(id=1),
                poi=poi,
                )
        photo.save()

def make_pois(modeladmin, request, queryset):
    added_pois = []
    for upresneni in queryset:
        poi = Poi(
                name=upresneni.name,
                desc=upresneni.desc,
                geom=upresneni.location,
                url=upresneni.url,
                address=upresneni.address,
                remark=u"Vytvořeno z upřesnění zadaného s emailem %s" % upresneni.email,
                marker=Marker.objects.get(slug='new'),
                )
        poi.save()
        make_photo(upresneni.photo1, upresneni.email, poi)
        make_photo(upresneni.photo2, upresneni.email, poi)
        make_photo(upresneni.photo3, upresneni.email, poi)
        added_pois.append(poi)

    added_pois_string = ", ".join([("<a href='/admin/webmap/poi/%s'>%s</a>" % (p.id, p.name)) for p in added_pois])
    modeladmin.message_user(request, mark_safe(u"Vytvořeny následující místa: %s" % added_pois_string))
make_pois.short_description = u"Vytvořit nová POI"


class UpresneniAdmin(OSMGeoAdmin):
    model = Upresneni
    raw_id_fields = ('webmap_poi',)
    list_filter = ('status',)
    list_display = ('webmap_poi', 'name', 'created', 'email', 'status', 'desc',)
    actions = [make_pois]


class StaticAdmin(admin.ModelAdmin):
    model = Staticpage

admin.site.unregister(Poi)
admin.site.register(Poi, Webmap_PoiAdmin)
admin.site.register(Upresneni, UpresneniAdmin)
admin.site.register(Staticpage, StaticAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

from comments_moderation import filtered_moderator
filtered_moderator.register(Poi)
