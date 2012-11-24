{% load mapwidget_tags %}var mapconfig = {};
mapconfig['vrstvy'] = [];
mapconfig['vrstvy'].push(["Město", "http://{% http_host %}/kml/mesto/"]);
mapconfig['vrstvy'].push(["Podniky", "http://{% http_host %}/kml/restaurace-kavarny/"]);
mapconfig['vrstvy'].push(["Obchody", "http://{% http_host %}/kml/obchody/"]);
mapconfig['vrstvy'].push(["Kultura", "http://{% http_host %}/kml/kultura/"]);
mapconfig['vrstvy'].push(["Komunity a NGO", "http://{% http_host %}/kml/komunity-ngo/"]);
mapconfig['vrstvy'].push(["Doprava", "http://{% http_host %}/kml/verejna-doprava/"]);

mapconfig['zoom'] = 16;
mapconfig['lon'] = {{obj.geom.get_x}};
mapconfig['lat'] = {{obj.geom.get_y}};
mapconfig['mapwidget'] = {}
mapconfig['mapwidget']["hide_controls"] = true;

//mapconfig['center_feature'] = {{obj.pk}};

//mapconfig['mobilni'] = true;