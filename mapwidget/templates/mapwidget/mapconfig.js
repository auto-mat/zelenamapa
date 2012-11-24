var mapconfig = {};
mapconfig['vrstvy'] = [];
mapconfig['vrstvy'].push(["Město", "/kml/mesto/"]);
mapconfig['vrstvy'].push(["Podniky", "/kml/restaurace-kavarny/"]);
mapconfig['vrstvy'].push(["Obchody", "/kml/obchody/"]);
mapconfig['vrstvy'].push(["Kultura", "/kml/kultura/"]);
mapconfig['vrstvy'].push(["Komunity a NGO", "/kml/komunity-ngo/"]);
mapconfig['vrstvy'].push(["Doprava", "/kml/verejna-doprava/"]);

mapconfig['zoom'] = 16;
mapconfig['lon'] = {{obj.geom.get_x}};
mapconfig['lat'] = {{obj.geom.get_y}};
mapconfig['mapwidget'] = {}
mapconfig['mapwidget']["hide_controls"] = true;

//mapconfig['center_feature'] = {{obj.pk}};

//mapconfig['mobilni'] = true;