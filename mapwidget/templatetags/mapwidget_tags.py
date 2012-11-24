import urllib2

from django import template
register = template.Library()

HTTP_HOST = "10.11.73.76:8033"

@register.simple_tag
def http_host():
    return HTTP_HOST