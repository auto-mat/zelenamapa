{% load mapwidget_tags %}var mapconfig = {};
mapconfig['vrstvy'] = [];
mapconfig['vrstvy'].push(["Město", "{{ SITE_URL }}/kml/mesto/"]);
mapconfig['vrstvy'].push(["Podniky", "{{ SITE_URL }}/kml/restaurace-kavarny/"]);
mapconfig['vrstvy'].push(["Obchody", "{{ SITE_URL }}/kml/obchody/"]);
mapconfig['vrstvy'].push(["Kultura", "{{ SITE_URL }}/kml/kultura/"]);
mapconfig['vrstvy'].push(["Komunity a NGO", "{{ SITE_URL }}/kml/komunity-ngo/"]);
mapconfig['vrstvy'].push(["Doprava", "{{ SITE_URL }}/kml/verejna-doprava/"]);

mapconfig['zoom'] = 16;
mapconfig['lon'] = {{obj.geom.get_x}};
mapconfig['lat'] = {{obj.geom.get_y}};
mapconfig['mapwidget'] = {}
mapconfig['mapwidget']["hide_controls"] = true;
mapconfig['site_url'] = "{{ SITE_URL }}";

//mapconfig['center_feature'] = {{obj.pk}};

//mapconfig['mobilni'] = true;
