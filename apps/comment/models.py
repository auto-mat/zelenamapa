from django.db import models

from mapa.models import Poi


class Comment(models.Model):
    poi = models.ForeignKey(Poi)
    name = models.CharField(max_length=64)
    email = models.EmailField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __unicode__(self):
        return u"%s (%s) ~%i %s" % (self.name, self.email, self.pk, self.content[:20])