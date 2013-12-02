# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName". 
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.

        for obj in orm.status.objects.all():
            obj_new, created = orm['webmap.status'].objects.get_or_create(name = obj.nazev, 
                    defaults={
                        'desc':           obj.desc,
                        'show':           obj.show,
                        'show_to_mapper': obj.show_TU,
                    }
                )
            obj_new.save()

        for obj in orm.vrstva.objects.all():
            obj_new, created = orm['webmap.layer'].objects.get_or_create(slug= obj.slug, 
                    defaults={
                        'name':           obj.nazev,
                        'slug':           obj.slug,
                        'desc':           obj.desc,
                        'status':         orm['webmap.status'].objects.get(name= obj.status.nazev),
                        'order':          obj.order,
                        'remark':         obj.remark,
                    }
                )
            obj_new.save()

        for obj in orm.znacka.objects.all():
            obj_new, created = orm['webmap.marker'].objects.get_or_create(name = obj.nazev,
                    defaults={
                        'layer':          orm['webmap.layer'].objects.get(slug= obj.vrstva.slug),
                        'status':         orm['webmap.status'].objects.get(name= obj.status.nazev),
                        'desc':           obj.desc,
                        'remark':         obj.remark,
                        'default_icon':   obj.default_icon,
                        'minzoom':        obj.minzoom,
                        'maxzoom':        obj.maxzoom,
                        'line_width':     obj.line_width,
                        'line_color':     obj.line_color,
                    }
                )
            obj_new.save()

        for obj in orm.sektor.objects.all():
            obj_new, created = orm['webmap.sector'].objects.get_or_create(slug = obj.slug,
                    defaults={
                        'name':           obj.nazev,
                        'geom':           obj.geom,
                    }
                )
            obj_new.save()

        for obj in orm.vlastnost.objects.all():
            obj_new, created = orm['webmap.property'].objects.get_or_create(name = obj.nazev,
                    defaults={
                        'status':         orm['webmap.status'].objects.get(name= obj.status.nazev),
                        'as_filter':      obj.filtr,
                        'order':          obj.poradi,
                        'slug':           obj.slug,
                        'desc':           obj.desc,
                        'remark':         obj.remark,
                        'default_icon':   obj.default_icon,
                    }
                )
            obj_new.save()

        for obj in orm.poi.objects.all():
            for field in obj_new._meta.local_fields:
                if field.name == "last_modification":
                    field.auto_now = False
                elif field.name == "created_at":
                    field.auto_now_add = False

            kwargs={
                'name':           obj.nazev,
                'marker':         orm['webmap.marker'].objects.get(name=obj.znacka.nazev),
                'status':         orm['webmap.status'].objects.get(name= obj.status.nazev),
                'importance':     obj.dulezitost,
                'geom':           obj.geom,
                'address':        obj.address,
                'desc':           obj.desc,
                'desc_extra':     obj.desc_extra,
                'url':            obj.url,
                'remark':         obj.remark,
                'properties_cache':obj.vlastnosti_cache,
                'last_modification':     obj.created_at,
                'created_at':     obj.created_at,
                'author':         obj.author,
            }

            obj_new = orm['webmap.poi'].objects.create(**kwargs)
            obj_new.properties = orm['webmap.property'].objects.filter(slug__in= [o.slug for o in obj.vlastnosti.all()])
            obj_new.save()

            for field in obj_new._meta.local_fields:
                if field.name == "last_modification":
                    field.auto_now = True
                elif field.name == "created_at":
                    field.auto_now_add = True

            if obj.foto_thumb:
                photo_new = orm['webmap.photo'].objects.create(poi = obj_new, photo = obj.foto_thumb, license_id=1, order=0)
                photo_new.save()

    def backwards(self, orm):
        "Write your backwards methods here."
        orm['webmap.photo'].objects.all().delete()
        orm['webmap.poi'].objects.all().delete()


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'webmap.layer': {
            'Meta': {'ordering': "['order']", 'object_name': 'Layer'},
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'remark': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webmap.Status']"})
        },
        'webmap.license': {
            'Meta': {'object_name': 'License'},
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'webmap.marker': {
            'Meta': {'ordering': "['-layer__order', 'name']", 'object_name': 'Marker'},
            'default_icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'layer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webmap.Layer']"}),
            'line_color': ('colorful.fields.RGBColorField', [], {'default': "'#ffc90e'", 'max_length': '7'}),
            'line_width': ('django.db.models.fields.FloatField', [], {'default': '2'}),
            'maxzoom': ('django.db.models.fields.PositiveIntegerField', [], {'default': '10'}),
            'minzoom': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'remark': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webmap.Status']"})
        },
        'webmap.photo': {
            'Meta': {'object_name': 'Photo'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'photo_create'", 'null': 'True', 'to': "orm['auth.User']"}),
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'license': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webmap.License']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'poi': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photos'", 'to': "orm['webmap.Poi']"}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'photo_update'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'webmap.poi': {
            'Meta': {'object_name': 'Poi'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'poi_create'", 'null': 'True', 'to': "orm['auth.User']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desc_extra': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.GeometryField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'importance': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'last_modification': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'marker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pois'", 'to': "orm['webmap.Marker']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'properties': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['webmap.Property']", 'null': 'True', 'blank': 'True'}),
            'properties_cache': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'remark': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'default': '2', 'to': "orm['webmap.Status']"}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'poi_update'", 'null': 'True', 'to': "orm['auth.User']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'webmap.property': {
            'Meta': {'ordering': "['order']", 'object_name': 'Property'},
            'as_filter': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'default_icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'remark': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webmap.Status']"})
        },
        'webmap.sector': {
            'Meta': {'object_name': 'Sector'},
            'geom': ('django.contrib.gis.db.models.fields.PolygonField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        'webmap.status': {
            'Meta': {'object_name': 'Status'},
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'show': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'show_to_mapper': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'mapa.poi': {
            'Meta': {'object_name': 'Poi'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desc_extra': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dulezitost': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'foto_thumb': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.GeometryField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nazev': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'remark': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sit_geom': ('django.contrib.gis.db.models.fields.GeometryField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'default': '2', 'to': "orm['mapa.Status']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'vlastnosti': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['mapa.Vlastnost']", 'null': 'True', 'blank': 'True'}),
            'vlastnosti_cache': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'znacka': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pois'", 'to': "orm['mapa.Znacka']"})
        },
        'mapa.sektor': {
            'Meta': {'ordering': "['nazev']", 'object_name': 'Sektor'},
            'geom': ('django.contrib.gis.db.models.fields.PolygonField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nazev': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        'mapa.sit': {
            'Meta': {'object_name': 'Sit'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'poi': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sit_keys'", 'to': "orm['mapa.Poi']"}),
            'value': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'mapa.staticpage': {
            'Meta': {'object_name': 'Staticpage'},
            'content': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'head': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'short': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'mapa.status': {
            'Meta': {'object_name': 'Status'},
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nazev': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'show': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'show_TU': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'mapa.upresneni': {
            'Meta': {'object_name': 'Upresneni'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'misto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mapa.Poi']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'mapa.vlastnost': {
            'Meta': {'ordering': "['poradi']", 'object_name': 'Vlastnost'},
            'default_icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'filtr': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nazev': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'poradi': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'remark': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mapa.Status']"})
        },
        'mapa.vrstva': {
            'Meta': {'ordering': "['order']", 'object_name': 'Vrstva'},
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nazev': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'remark': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mapa.Status']"})
        },
        'mapa.znacka': {
            'Meta': {'ordering': "['-vrstva__order', 'nazev']", 'object_name': 'Znacka'},
            'default_icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line_color': ('colorful.fields.RGBColorField', [], {'default': "'#ffc90e'", 'max_length': '7'}),
            'line_width': ('django.db.models.fields.FloatField', [], {'default': '2'}),
            'maxzoom': ('django.db.models.fields.PositiveIntegerField', [], {'default': '10'}),
            'minzoom': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'mobile_icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'nazev': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'remark': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mapa.Status']"}),
            'vrstva': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mapa.Vrstva']"})
        }
    }

    complete_apps = ['webmap', 'mapa']
    symmetrical = True
