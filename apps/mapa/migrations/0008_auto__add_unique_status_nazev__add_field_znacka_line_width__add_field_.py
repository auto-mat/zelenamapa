# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Status', fields ['nazev']
        db.create_unique(u'mapa_status', ['nazev'])

        # Adding field 'Znacka.line_width'
        db.add_column(u'mapa_znacka', 'line_width',
                      self.gf('django.db.models.fields.FloatField')(default=2),
                      keep_default=False)

        # Adding field 'Znacka.line_color'
        db.add_column(u'mapa_znacka', 'line_color',
                      self.gf('colorful.fields.RGBColorField')(default='#ffc90e', max_length=7),
                      keep_default=False)

        # Adding unique constraint on 'Znacka', fields ['nazev']
        db.create_unique(u'mapa_znacka', ['nazev'])


    def backwards(self, orm):
        # Removing unique constraint on 'Znacka', fields ['nazev']
        db.delete_unique(u'mapa_znacka', ['nazev'])

        # Removing unique constraint on 'Status', fields ['nazev']
        db.delete_unique(u'mapa_status', ['nazev'])

        # Deleting field 'Znacka.line_width'
        db.delete_column(u'mapa_znacka', 'line_width')

        # Deleting field 'Znacka.line_color'
        db.delete_column(u'mapa_znacka', 'line_color')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'mapa.poi': {
            'Meta': {'object_name': 'Poi'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desc_extra': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dulezitost': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'foto_thumb': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.GeometryField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nazev': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'remark': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sit_geom': ('django.contrib.gis.db.models.fields.GeometryField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'default': '2', 'to': u"orm['mapa.Status']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'vlastnosti': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['mapa.Vlastnost']", 'null': 'True', 'blank': 'True'}),
            'vlastnosti_cache': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'znacka': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pois'", 'to': u"orm['mapa.Znacka']"})
        },
        u'mapa.sektor': {
            'Meta': {'object_name': 'Sektor'},
            'geom': ('django.contrib.gis.db.models.fields.PolygonField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nazev': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'mapa.sit': {
            'Meta': {'object_name': 'Sit'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'poi': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sit_keys'", 'to': u"orm['mapa.Poi']"}),
            'value': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'mapa.staticpage': {
            'Meta': {'object_name': 'Staticpage'},
            'content': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'head': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'short': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'mapa.status': {
            'Meta': {'object_name': 'Status'},
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nazev': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'show': ('django.db.models.fields.BooleanField', [], {}),
            'show_TU': ('django.db.models.fields.BooleanField', [], {})
        },
        u'mapa.upresneni': {
            'Meta': {'object_name': 'Upresneni'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'misto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mapa.Poi']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'mapa.vlastnost': {
            'Meta': {'ordering': "['poradi']", 'object_name': 'Vlastnost'},
            'default_icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'filtr': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nazev': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'poradi': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'remark': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mapa.Status']"})
        },
        u'mapa.vrstva': {
            'Meta': {'ordering': "['order']", 'object_name': 'Vrstva'},
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nazev': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'remark': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mapa.Status']"})
        },
        u'mapa.znacka': {
            'Meta': {'ordering': "['-vrstva__order', 'nazev']", 'object_name': 'Znacka'},
            'default_icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line_color': ('colorful.fields.RGBColorField', [], {'default': "'#ffc90e'", 'max_length': '7'}),
            'line_width': ('django.db.models.fields.FloatField', [], {'default': '2'}),
            'maxzoom': ('django.db.models.fields.PositiveIntegerField', [], {'default': '10'}),
            'minzoom': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'mobile_icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'nazev': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'remark': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mapa.Status']"}),
            'vrstva': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mapa.Vrstva']"})
        }
    }

    complete_apps = ['mapa']