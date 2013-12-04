# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Poi'
        db.delete_table('mapa_poi')

        # Removing M2M table for field vlastnosti on 'Poi'
        db.delete_table(db.shorten_name('mapa_poi_vlastnosti'))

        # Deleting model 'Vrstva'
        db.delete_table('mapa_vrstva')

        # Deleting model 'Status'
        db.delete_table('mapa_status')

        # Deleting model 'Znacka'
        db.delete_table('mapa_znacka')

        # Deleting model 'Sektor'
        db.delete_table('mapa_sektor')

        # Deleting model 'Vlastnost'
        db.delete_table('mapa_vlastnost')

        # Deleting field 'Upresneni.misto'
        db.delete_column('mapa_upresneni', 'misto_id')

        # Deleting field 'Sit.poi'
        db.delete_column('mapa_sit', 'poi_id')


    def backwards(self, orm):
        # Adding model 'Poi'
        db.create_table('mapa_poi', (
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(default=2, to=orm['mapa.Status'])),
            ('remark', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('znacka', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pois', to=orm['mapa.Znacka'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('dulezitost', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('nazev', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('vlastnosti_cache', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('desc_extra', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('geom', self.gf('django.contrib.gis.db.models.fields.GeometryField')()),
            ('foto_thumb', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('sit_geom', self.gf('django.contrib.gis.db.models.fields.GeometryField')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('desc', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('mapa', ['Poi'])

        # Adding M2M table for field vlastnosti on 'Poi'
        m2m_table_name = db.shorten_name('mapa_poi_vlastnosti')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('poi', models.ForeignKey(orm['mapa.poi'], null=False)),
            ('vlastnost', models.ForeignKey(orm['mapa.vlastnost'], null=False))
        ))
        db.create_unique(m2m_table_name, ['poi_id', 'vlastnost_id'])

        # Adding model 'Vrstva'
        db.create_table('mapa_vrstva', (
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mapa.Status'])),
            ('remark', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, unique=True)),
            ('nazev', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('desc', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('mapa', ['Vrstva'])

        # Adding model 'Status'
        db.create_table('mapa_status', (
            ('show', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('nazev', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True)),
            ('show_TU', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('desc', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('mapa', ['Status'])

        # Adding model 'Znacka'
        db.create_table('mapa_znacka', (
            ('line_color', self.gf('colorful.fields.RGBColorField')(default='#ffc90e', max_length=7)),
            ('mobile_icon', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('nazev', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True)),
            ('minzoom', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('maxzoom', self.gf('django.db.models.fields.PositiveIntegerField')(default=10)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('desc', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('line_width', self.gf('django.db.models.fields.FloatField')(default=2)),
            ('remark', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('vrstva', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mapa.Vrstva'])),
            ('default_icon', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mapa.Status'])),
        ))
        db.send_create_signal('mapa', ['Znacka'])

        # Adding model 'Sektor'
        db.create_table('mapa_sektor', (
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, unique=True)),
            ('geom', self.gf('django.contrib.gis.db.models.fields.PolygonField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nazev', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('mapa', ['Sektor'])

        # Adding model 'Vlastnost'
        db.create_table('mapa_vlastnost', (
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mapa.Status'])),
            ('remark', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('poradi', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, unique=True)),
            ('nazev', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('default_icon', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
            ('filtr', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('desc', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('mapa', ['Vlastnost'])

        # Adding field 'Upresneni.misto'
        db.add_column('mapa_upresneni', 'misto',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mapa.Poi'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Sit.poi'
        db.add_column('mapa_sit', 'poi',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['mapa.Poi']),
                      keep_default=False)


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
        'mapa.sit': {
            'Meta': {'object_name': 'Sit'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'value': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'webmap_poi': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webmap.Poi']", 'null': 'True', 'blank': 'True'})
        },
        'mapa.sitpoi': {
            'Meta': {'object_name': 'SitPoi'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sit_geom': ('django.contrib.gis.db.models.fields.GeometryField', [], {'null': 'True', 'blank': 'True'}),
            'webmap_poi': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['webmap.Poi']", 'unique': 'True'})
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
        'mapa.upresneni': {
            'Meta': {'object_name': 'Upresneni'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'webmap_poi': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webmap.Poi']", 'null': 'True', 'blank': 'True'})
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
        'webmap.status': {
            'Meta': {'object_name': 'Status'},
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'show': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'show_to_mapper': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['mapa']