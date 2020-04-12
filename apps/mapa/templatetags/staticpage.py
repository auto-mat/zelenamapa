from django import template
from mapa.models import Staticpage

register = template.Library()

class GetStaticPageNode(template.Node):
    def __init__(self, slug, variable):
        self.slug = slug
        self.variable = variable

    def render(self, context):
        context[self.variable] = Staticpage.objects.get(slug=self.slug)
        return ''

@register.tag
def get_staticpage(parser, token):
    "Najde a vrati Staticpage podle slugu"
    bits = token.split_contents()
    if len(bits) != 4:
        raise template.TemplateSyntaxError("%r tag takes exactly three arguments" % bits[0])
    if bits[2] != 'as':
        raise template.TemplateSyntaxError("second argument to %r tag must be 'as'" % bits[0])
    slug = bits[1]
    if not (slug[0] == slug[-1] and slug[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % bits[0])
    return GetStaticPageNode(slug[1:-1], bits[3])
