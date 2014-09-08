# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('webmap', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(default=b'', max_length=255, verbose_name='key')),
                ('value', models.CharField(default=b'', max_length=255, null=True, verbose_name='value', blank=True)),
                ('webmap_poi', models.ForeignKey(blank=True, to='webmap.Poi', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SitPoi',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sit_geom', django.contrib.gis.db.models.fields.GeometryField(help_text='P\u016fvodn\xed poloha podle SITu', srid=4326, null=True, verbose_name='SIT poloha', blank=True)),
                ('webmap_poi', models.OneToOneField(to='webmap.Poi')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Staticpage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, verbose_name=b'Slug')),
                ('head', models.TextField(null=True, verbose_name='Header section (additional css, js, etc.)', blank=True)),
                ('title', models.CharField(max_length=255, null=True, verbose_name='Titulek straky', blank=True)),
                ('short', models.TextField(null=True, verbose_name='Zkraceny html obsah (nahled)')),
                ('content', models.TextField(null=True, verbose_name='Html obsah')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Upresneni',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=75, null=True, verbose_name='V\xe1\u0161 e-mail (pro dal\u0161\xed komunikaci)')),
                ('status', models.CharField(max_length=10, choices=[(b'novy', 'Nov\xfd'), (b'reseno', 'V \u0159e\u0161en\xed'), (b'vyreseno', 'Vy\u0159e\u0161eno'), (b'zamitnuto', 'Zam\xedtnuto')])),
                ('desc', models.TextField(null=True, verbose_name='Popis (dopln\u011bn\xed nebo oprava nebo popis nov\xe9ho m\xedsta, povinn\xe9 pole)')),
                ('url', models.URLField(null=True, verbose_name='Odkaz, webov\xe9 str\xe1nky m\xedsta (voliteln\xe9 pole)', blank=True)),
                ('address', models.CharField(max_length=255, null=True, verbose_name='Adresa m\xedsta, popis lokace (voliteln\xe9 pole)', blank=True)),
                ('webmap_poi', models.ForeignKey(blank=True, to='webmap.Poi', null=True)),
            ],
            options={
                'verbose_name_plural': 'up\u0159esn\u011bn\xed',
            },
            bases=(models.Model,),
        ),
    ]
