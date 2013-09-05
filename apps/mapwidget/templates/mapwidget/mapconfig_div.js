{% load mapwidget_tags %}

function loadScript(url, callback)
{
    // adding the script tag to the head as suggested before
   var head = document.getElementsByTagName('head')[0];
   var script = document.createElement('script');
   script.type = 'text/javascript';
   script.src = url;

   // then bind the event to the callback function 
   // there are several events for cross browser compatibility
   script.onreadystatechange = callback;
   script.onload = callback;

   // fire the loading
   head.appendChild(script);
}

var mapconfig = {};
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

loadScript("{{ SITE_URL }}/static/js/OpenLayers.js", function(){
   loadScript("{{ SITE_URL }}/static/js/OpenStreetMap.js", function(){
      loadScript("{{ SITE_URL }}/static/js/MyFramedCloud.js", function(){
         loadScript("{{ SITE_URL }}/static/js/jquery.tools.min.js", function(){
            loadScript("{{ SITE_URL }}/static/js/jquery.ba-hashchange.min.js", function(){
            loadScript("{{ SITE_URL }}/static/js/mapa.js", function(){
               
               $(document).ready(function(){init(mapconfig);})
})})})})})});

