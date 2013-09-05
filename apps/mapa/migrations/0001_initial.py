# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Status'
        db.create_table('mapa_status', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nazev', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('desc', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('show', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('show_TU', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('mapa', ['Status'])

        # Adding model 'Vrstva'
        db.create_table('mapa_vrstva', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nazev', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('desc', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mapa.Status'])),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('remark', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('mapa', ['Vrstva'])

        # Adding model 'Znacka'
        db.create_table('mapa_znacka', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nazev', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('vrstva', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mapa.Vrstva'])),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mapa.Status'])),
            ('desc', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('remark', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('default_icon', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
            ('minzoom', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('maxzoom', self.gf('django.db.models.fields.PositiveIntegerField')(default=10)),
        ))
        db.send_create_signal('mapa', ['Znacka'])

        # Adding model 'Poi'
        db.create_table('mapa_poi', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nazev', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('znacka', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mapa.Znacka'])),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mapa.Status'])),
            ('dulezitost', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('geom', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('desc', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('desc_extra', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('remark', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('foto_thumb', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('vlastnosti_cache', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('mapa', ['Poi'])

        # Adding M2M table for field vlastnosti on 'Poi'
        db.create_table('mapa_poi_vlastnosti', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('poi', models.ForeignKey(orm['mapa.poi'], null=False)),
            ('vlastnost', models.ForeignKey(orm['mapa.vlastnost'], null=False))
        ))
        db.create_unique('mapa_poi_vlastnosti', ['poi_id', 'vlastnost_id'])

        # Adding model 'Vlastnost'
        db.create_table('mapa_vlastnost', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nazev', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mapa.Status'])),
            ('filtr', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('poradi', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('desc', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('remark', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('default_icon', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
        ))
        db.send_create_signal('mapa', ['Vlastnost'])

        # Adding model 'Upresneni'
        db.create_table('mapa_upresneni', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('misto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mapa.Poi'], null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('desc', self.gf('django.db.models.fields.TextField')(null=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('mapa', ['Upresneni'])

        # Adding model 'Staticpage'
        db.create_table('mapa_staticpage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('head', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('short', self.gf('django.db.models.fields.TextField')(null=True)),
            ('content', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('mapa', ['Staticpage'])


    def backwards(self, orm):
        # Deleting model 'Status'
        db.delete_table('mapa_status')

        # Deleting model 'Vrstva'
        db.delete_table('mapa_vrstva')

        # Deleting model 'Znacka'
        db.delete_table('mapa_znacka')

        # Deleting model 'Poi'
        db.delete_table('mapa_poi')

        # Removing M2M table for field vlastnosti on 'Poi'
        db.delete_table('mapa_poi_vlastnosti')

        # Deleting model 'Vlastnost'
        db.delete_table('mapa_vlastnost')

        # Deleting model 'Upresneni'
        db.delete_table('mapa_upresneni')

        # Deleting model 'Staticpage'
        db.delete_table('mapa_staticpage')


    models = {
        'mapa.poi': {
            'Meta': {'object_name': 'Poi'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desc_extra': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dulezitost': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'foto_thumb': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nazev': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'remark': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mapa.Status']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'vlastnosti': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['mapa.Vlastnost']", 'null': 'True', 'blank': 'True'}),
            'vlastnosti_cache': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'znacka': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mapa.Znacka']"})
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
            'nazev': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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
            'Meta': {'object_name': 'Znacka'},
            'default_icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maxzoom': ('django.db.models.fields.PositiveIntegerField', [], {'default': '10'}),
            'minzoom': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'nazev': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'remark': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mapa.Status']"}),
            'vrstva': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mapa.Vrstva']"})
        }
    }

    complete_apps = ['mapa']