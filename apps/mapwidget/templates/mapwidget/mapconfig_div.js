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
mapconfig['vrstvy'].push(["Město", "http://{{ site }}/kml/mesto/"]);
mapconfig['vrstvy'].push(["Podniky", "http://{{ site }}/kml/restaurace-kavarny/"]);
mapconfig['vrstvy'].push(["Obchody", "http://{{ site }}/kml/obchody/"]);
mapconfig['vrstvy'].push(["Kultura", "http://{{ site }}/kml/kultura/"]);
mapconfig['vrstvy'].push(["Komunity a NGO", "http://{{ site }}/kml/komunity-ngo/"]);
mapconfig['vrstvy'].push(["Doprava", "http://{{ site }}/kml/verejna-doprava/"]);

mapconfig['zoom'] = 16;
mapconfig['lon'] = {{obj.geom.get_x}};
mapconfig['lat'] = {{obj.geom.get_y}};
mapconfig['mapwidget'] = {}
mapconfig['mapwidget']["hide_controls"] = true;
mapconfig['site_url'] = "http://{{ site }}";

loadScript("http://{{ site }}/static/js/OpenLayers.js", function(){
   loadScript("http://{{ site }}/static/js/OpenStreetMap.js", function(){
      loadScript("http://{{ site }}/static/js/MyFramedCloud.js", function(){
         loadScript("http://{{ site }}/static/js/jquery.tools.min.js", function(){
            loadScript("http://{{ site }}/static/js/jquery.ba-hashchange.min.js", function(){
            loadScript("http://{{ site }}/static/js/mapa.js", function(){
               
               mapconfig['bounds'] = new OpenLayers.Bounds( {{ config.MAP_BOUNDS }});
               $(document).ready(function(){init(mapconfig);})
})})})})})});

