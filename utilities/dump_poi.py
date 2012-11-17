import os, sys
import csv,codecs, cStringIO

PROJECTDIR = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]

sys.path.append(PROJECTDIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from mapa.models import *
#writer = csv.writer(open('mista.csv', 'wb'), delimiter=';')

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

import codecs
#f = codecs.open('mista.csv', 'w', encoding="utf-8")
f = open('mista.csv', 'w')
writer = UnicodeWriter(f, delimiter=';')


header = [
        'nazev',
        'znacka',
        'url',
        'adresa',
        'popis',
        'interni pozn.',
        'vlastnosti',
]
for v in Vlastnost.objects.all().order_by('id'):
   header.append(v.nazev)
writer.writerow(header)

for p in Poi.viditelne.all():
   row = [
       p.nazev,
       p.znacka.nazev,
       p.url,
       p.address,
       p.desc,
       p.remark,
       p.vlastnosti_cache,
   ]
   for v in Vlastnost.objects.all().order_by('id'):
       if v.slug in p.vlastnosti_cache:
           row.append(u'A')
       else:
           row.append(u'N')
   writer.writerow(row)
