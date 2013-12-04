# -*- coding: utf-8 -*-
# admin.py

from django.conf import settings # needed if we use the GOOGLE_MAPS_API_KEY from settings

# Import the admin site reference from django.contrib.admin
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from webmap.models import Poi
import webmap
from django.contrib.auth.models import User
from mapa.models import Upresneni, Staticpage, Sit, SitPoi

class UserAdmin(UserAdmin):
    list_display = ('__unicode__', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active', 'last_login', 'get_groups', 'get_user_permissions')

    def get_groups(self, obj):
        if obj:
            return ", ".join([group.name for group in obj.groups.all()])

    def get_user_permissions(self, obj):
        if obj:
            return ", ".join([user_permission.name for user_permission in obj.user_permissions.all()])

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
    inlines = webmap.admin.PoiAdmin.inlines + [ SitPoiInline, SitInline, ]

class UpresneniAdmin(admin.ModelAdmin):
    model = Upresneni
    raw_id_fields = ('webmap_poi',)
    list_filter = ('status',)
    list_display = ('webmap_poi', 'email', 'status', 'desc',)

class StaticAdmin(admin.ModelAdmin):
    model = Staticpage
    
admin.site.unregister(Poi)
admin.site.register(Poi   , Webmap_PoiAdmin   )
admin.site.register(Upresneni, UpresneniAdmin)
admin.site.register(Staticpage, StaticAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

from comments_moderation import filtered_moderator
filtered_moderator.register(Poi)
