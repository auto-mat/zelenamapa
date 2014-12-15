{% load cache %}

{% cache 86400 mapconfig %} {# 24 hodin #}
    var mapconfig = {};
    mapconfig['vrstvy'] = [];
    {% for v in vrstvy %}
        mapconfig['vrstvy'].push(["{{v.name}}", "http://{{ site }}{% url 'webmap.views.kml_view' v.slug %}"]);
    {% endfor %}
{% endcache %}

mapconfig['siteurl'] = "http://{{ site }}";
mapconfig['basezoom'] = {{ config.MAP_BASEZOOM }};
mapconfig['baselon'] = {{ config.MAP_BASELON }};
mapconfig['baselat'] = {{ config.MAP_BASELAT }};
mapconfig['bounds'] = new OpenLayers.Bounds( {{ config.MAP_BOUNDS }});
mapconfig['minzoom'] = {{ config.MIN_ZOOMLEVEL }};
{% if center_poi %}
    mapconfig['zoom'] = {{ config.MAP_POIZOOM }};
    mapconfig['lon'] = {{ center_poi.geom.x }};
    mapconfig['lat'] = {{ center_poi.geom.y }};
    mapconfig['center_feature'] = {{ center_poi.id }};
{% else %}
    mapconfig['zoom'] = mapconfig['basezoom'];
    mapconfig['lon'] = mapconfig['baselon'];
    mapconfig['lat'] = mapconfig['baselat'];
{% endif %}
{% if mobilni %}
    mapconfig['mobilni'] = true;
{% else %}
    mapconfig['mobilni'] = false;
{% endif %}
