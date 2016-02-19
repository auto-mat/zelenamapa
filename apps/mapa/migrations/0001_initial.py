# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import colorful.fields
import django.contrib.gis.db.models.fields
from django.conf import settings
import mapa.utils


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Poi',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'Posledni zmena')),
                ('nazev', models.CharField(help_text='P\u0159esn\xfd n\xe1zev m\xedsta.', max_length=255, verbose_name='n\xe1zev')),
                ('dulezitost', models.SmallIntegerField(default=0, help_text='Modifik\xe1tor minimalniho zoomu, ve kter\xe9m se m\xedsto zobrazuje (20+ bude vid\u011bt v\u017edy).<br/>\n                               C\xedl je m\xedt v\xfdb\u011br z\xe1kladn\xedch objekt\u016f viditeln\xfdch ve velk\xfdch m\u011b\u0159\xedtc\xedch\n                               a zabr\xe1nit p\u0159et\xed\u017een\xed mapy zna\u010dkami v p\u0159ehledce.<br/>\n                               Lze pou\u017e\xedt pro placenou reklamu! ("V\xe1\u0161 podnik bude vid\u011bt hned po otev\u0159en\xed mapy")', verbose_name='d\u016fle\u017eitost')),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(help_text='Vlo\u017een\xed bodu: Klikn\u011bte na tu\u017eku s plusem a um\xedst\u011bte bod na mapu.', srid=4326, verbose_name='poloha')),
                ('desc', models.TextField(help_text='Text, kter\xfd se zobraz\xed na map\u011b po kliknut\xed na ikonu.', null=True, verbose_name='popis', blank=True)),
                ('desc_extra', models.TextField(help_text=b'Text, kter\xc3\xbd roz\xc5\xa1i\xc5\x99uje informace v\xc3\xbd\xc5\xa1e.', null=True, verbose_name='podrobn\xfd popis', blank=True)),
                ('url', models.URLField(help_text='Odkaz na webovou str\xe1nku m\xedsta.', null=True, blank=True)),
                ('address', models.CharField(help_text='Adresa m\xedsta (ulice, \u010d\xedslo domu)', max_length=255, null=True, verbose_name='adresa', blank=True)),
                ('remark', models.TextField(help_text='Intern\xed informace o objektu, kter\xe9 se nebudou zobrazovat.', null=True, verbose_name='intern\xed pozn\xe1mka', blank=True)),
                ('foto_thumb', models.ImageField(storage=mapa.utils.SlugifyFileSystemStorage(), upload_to=b'foto', blank=True, help_text='Nahrajte fotku v pln\xe9 velikosti.', null=True, verbose_name='fotka')),
                ('vlastnosti_cache', models.CharField(max_length=255, null=True, blank=True)),
                ('sit_geom', django.contrib.gis.db.models.fields.GeometryField(help_text='P\u016fvodn\xed poloha podle SITu', srid=4326, null=True, verbose_name='SIT poloha', blank=True)),
                ('author', models.ForeignKey(verbose_name=b'Autor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'm\xedsto',
                'verbose_name_plural': 'm\xedsta',
                'permissions': [('can_only_own_data_only', 'Can only edit his own data'), ('can_edit_advanced_fields', 'Can edit dulezitost status')],
            },
        ),
        migrations.CreateModel(
            name='Sektor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nazev', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True, verbose_name=b'Slug')),
                ('geom', django.contrib.gis.db.models.fields.PolygonField(help_text='Plocha sektoru', srid=4326, verbose_name='plocha')),
            ],
            options={
                'ordering': ['nazev'],
                'verbose_name_plural': 'sektory',
            },
        ),
        migrations.CreateModel(
            name='Sit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(default=b'', max_length=255, verbose_name='key')),
                ('value', models.CharField(default=b'', max_length=255, null=True, verbose_name='value', blank=True)),
                ('poi', models.ForeignKey(related_name='sit_keys', to='mapa.Poi')),
            ],
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
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nazev', models.CharField(help_text='N\xe1zev statutu', unique=True, max_length=255)),
                ('desc', models.TextField(help_text='Popis', null=True, blank=True)),
                ('show', models.BooleanField(help_text='Zobrazit u\u017eivateli zven\u010d\xed')),
                ('show_TU', models.BooleanField(help_text='Zobrazit editorovi mapy')),
            ],
            options={
                'verbose_name_plural': 'statuty',
            },
        ),
        migrations.CreateModel(
            name='Upresneni',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='V\xe1\u0161 e-mail (pro dal\u0161\xed komunikaci)')),
                ('status', models.CharField(max_length=10, choices=[(b'novy', 'Nov\xfd'), (b'reseno', 'V \u0159e\u0161en\xed'), (b'vyreseno', 'Vy\u0159e\u0161eno'), (b'zamitnuto', 'Zam\xedtnuto')])),
                ('desc', models.TextField(null=True, verbose_name='Popis (dopln\u011bn\xed nebo oprava nebo popis nov\xe9ho m\xedsta, povinn\xe9 pole)')),
                ('url', models.URLField(null=True, verbose_name='Odkaz, webov\xe9 str\xe1nky m\xedsta (voliteln\xe9 pole)', blank=True)),
                ('address', models.CharField(max_length=255, null=True, verbose_name='Adresa m\xedsta, popis lokace (voliteln\xe9 pole)', blank=True)),
                ('misto', models.ForeignKey(blank=True, to='mapa.Poi', null=True)),
            ],
            options={
                'verbose_name_plural': 'up\u0159esn\u011bn\xed',
            },
        ),
        migrations.CreateModel(
            name='Vlastnost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nazev', models.CharField(max_length=255)),
                ('filtr', models.BooleanField()),
                ('poradi', models.PositiveIntegerField()),
                ('slug', models.SlugField(unique=True, verbose_name=b'Slug')),
                ('desc', models.TextField(null=True, blank=True)),
                ('remark', models.TextField(help_text='interni informace o objektu, ktere se nebudou zobrazovat', null=True, blank=True)),
                ('default_icon', models.ImageField(storage=mapa.utils.SlugifyFileSystemStorage(), null=True, upload_to=b'ikony')),
                ('status', models.ForeignKey(to='mapa.Status')),
            ],
            options={
                'ordering': ['poradi'],
                'verbose_name_plural': 'vlastnosti',
            },
        ),
        migrations.CreateModel(
            name='Vrstva',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nazev', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True, verbose_name='n\xe1zev v URL')),
                ('desc', models.TextField(null=True, blank=True)),
                ('order', models.PositiveIntegerField()),
                ('remark', models.TextField(help_text='interni informace o objektu, ktere se nebudou zobrazovat', null=True, blank=True)),
                ('status', models.ForeignKey(to='mapa.Status')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name_plural': 'vrstvy',
            },
        ),
        migrations.CreateModel(
            name='Znacka',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nazev', models.CharField(unique=True, max_length=255)),
                ('desc', models.TextField(help_text='podrobny popis znacky', null=True, blank=True)),
                ('remark', models.TextField(help_text='interni informace o objektu, ktere se nebudou zobrazovat', null=True, blank=True)),
                ('default_icon', models.ImageField(storage=mapa.utils.SlugifyFileSystemStorage(), null=True, upload_to=b'ikony', blank=True)),
                ('mobile_icon', models.ImageField(storage=mapa.utils.SlugifyFileSystemStorage(), null=True, upload_to=b'ikony_m', blank=True)),
                ('minzoom', models.PositiveIntegerField(default=1)),
                ('maxzoom', models.PositiveIntegerField(default=10)),
                ('line_width', models.FloatField(default=2, verbose_name='\u0161\xed\u0159ka \u010d\xe1ry')),
                ('line_color', colorful.fields.RGBColorField(default=b'#ffc90e')),
                ('status', models.ForeignKey(to='mapa.Status')),
                ('vrstva', models.ForeignKey(to='mapa.Vrstva')),
            ],
            options={
                'ordering': ['-vrstva__order', 'nazev'],
                'verbose_name_plural': 'zna\u010dky',
                'permissions': [('can_only_view', 'Can only view')],
            },
        ),
        migrations.AddField(
            model_name='poi',
            name='status',
            field=models.ForeignKey(default=2, to='mapa.Status', help_text=b'Status m\xc3\xadsta; ur\xc4\x8duje, kde v\xc5\xa1ude se m\xc3\xadsto zobraz\xc3\xad.'),
        ),
        migrations.AddField(
            model_name='poi',
            name='vlastnosti',
            field=models.ManyToManyField(help_text=b'Ur\xc4\x8dete, jak\xc3\xa9 m\xc3\xa1 m\xc3\xadsto vlastnosti. Postupujte podle manu\xc3\xa1lu.<br/>', to='mapa.Vlastnost', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='poi',
            name='znacka',
            field=models.ForeignKey(related_name='pois', verbose_name='zna\u010dka', to='mapa.Znacka', help_text=b'Zde vyberte ikonu, kter\xc3\xa1 se zobraz\xc3\xad na map\xc4\x9b.'),
        ),
    ]
