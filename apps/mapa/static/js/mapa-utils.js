
function getTileURL(bounds)
{
	var res = this.map.getResolution();
	var x = Math.round((bounds.left - this.maxExtent.left) / (res * this.tileSize.w));
	var y = Math.round((this.maxExtent.top - bounds.top) / (res * this.tileSize.h));
	var z = this.map.getZoom();
	return this.url + z + "/" + x + "/" + y + "." + this.type;
}

function resizeIframe(obj) {
   obj.style.height = obj.contentWindow.document.body.scrollHeight + 30 + 'px';
};

function printAreaChanged(){
   top_ = parseInt($("#print_area").css("top"));
   left = parseInt($("#print_area").css("left"));
   width = parseInt($("#print_area").css("width"));
   height = parseInt($("#print_area").css("height"));
   orientation = height > width ? "portrait" : "landscape";
   $('#print_style').remove();
   $('head').append('<style type="text/css" media="print" id="print_style">#map{width:' + (width + left) + 'px;height:' + (height + top_) + 'px; top: -' + top_ + 'px; left: -' + left + 'px;} .olControlScaleLine, .olControlAttribution { left: ' + (left + 10) + 'px !important; } @page {size: ' + orientation + ';}</style>');
};

function noEventStart(){
   $("#noevent_area").show();
}
function noEventStop(){
   $("#noevent_area").hide();
}

function getUrlVars()
{
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
}

function loadTabs(){
  $( "#tabs" ).tabs({
    activate: function(event, ui) {
       selectedTab = ui.newTab.index();
       if(selectedTab == 2){
          $('#print_area').show();
       } else {
          $('#print_area').hide();
       };
    }
  });
}

function loadPrintArea(){
  $('#print_area').resizable({
     resize: printAreaChanged,
     start: noEventStart,
     stop: noEventStop
  }).draggable({
     drag: printAreaChanged,
     start: noEventStart,
     stop: noEventStop
  });
}
