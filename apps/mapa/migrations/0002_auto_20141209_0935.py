# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.contrib.gis.db.models.fields
import webmap.utils


class Migration(migrations.Migration):

    dependencies = [
        ('mapa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='upresneni',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 9, 9, 35, 8, 56827), verbose_name=b'created at', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='upresneni',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(help_text='Poloha p\u0159id\xe1van\xe9ho m\xedsta', srid=4326, null=True, verbose_name='poloha', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='upresneni',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 9, 9, 35, 12, 192607), verbose_name=b'last modification at', auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='upresneni',
            name='name',
            field=models.CharField(default='', max_length=255, verbose_name=b'N\xc3\xa1zev'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='upresneni',
            name='photo1',
            field=models.ImageField(storage=webmap.utils.SlugifyFileSystemStorage(), upload_to=b'photo_upload', null=True, verbose_name=b'Foto 1', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='upresneni',
            name='photo2',
            field=models.ImageField(storage=webmap.utils.SlugifyFileSystemStorage(), upload_to=b'photo_upload', null=True, verbose_name=b'Foto 2', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='upresneni',
            name='photo3',
            field=models.ImageField(storage=webmap.utils.SlugifyFileSystemStorage(), upload_to=b'photo_upload', null=True, verbose_name=b'Foto 3', blank=True),
            preserve_default=True,
        ),
    ]
