import urllib2

from django import template
register = template.Library()

REQUEST_HTTP_HOST = "10.11.73.76:8033"

@register.simple_tag
def include_url(url):
    try: return urllib2.urlopen(url).read()
    except: pass
    try: return urllib2.urlopen("http://%s%s"%(REQUEST_HTTP_HOST, url)).read()  # XXX: fixed
    except: pass
    return ""