from django import template

register = template.Library()

@register.simple_tag
def geturl(url, timeout=None):
    """
    Usage: {% geturl url [timeout] %}

    Examples:
    {% geturl "http://example.com/path/to/content/" %}
    {% geturl object.urlfield 1 %} 
    """
    import socket
    from urllib.request import urlopen
    socket_default_timeout = socket.getdefaulttimeout()
    if timeout is not None:
        try:
            socket_timeout = float(timeout)
        except ValueError:
            raise template.TemplateSyntaxError("timeout argument of geturl tag, if provided, must be convertible to a float")
        try:
            socket.setdefaulttimeout(socket_timeout)
        except ValueError:
            raise template.TemplateSyntaxError("timeout argument of geturl tag, if provided, cannot be less than zero")
    try:
        try: 
            content = urlopen(url).read()
        finally: # reset socket timeout
            if timeout is not None:
                socket.setdefaulttimeout(socket_default_timeout) 
    except:
        content = ''        
    return content
