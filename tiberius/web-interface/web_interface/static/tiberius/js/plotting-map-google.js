/*
Template Name: Color Admin - Responsive Admin Dashboard Template build with Twitter Bootstrap 3.3.5
Version: 1.9.0
Author: Sean Ngu
Website: http://www.seantheme.com/color-admin-v1.9/admin/
*/

var handleGoogleMapSetting = function(mission_id) {
	"use strict";
	var map;
	var poly;
	var stuff = [];

	function getWaypoints(){
		return JSON.stringify(stuff);
	}

	// $('#btn-submit').click(function(){
	//
	// }

	$('#btn-save-plot').click(function(){
		var data = stuff;
		var URL = "/missionplanner/plotting/" + mission_id + "/";
		$.ajax({
				url: URL,
				type: 'POST',
				data: {
								'waypoints': JSON.stringify(data),
								'mission_id': mission_id
							},
				success: function (result) {
					alert(result);
					document.open();
					document.write(result);
					document.close();
				},
				error: function(error_msg){
					alert("ERROR");
				}
		});
	});

	function MarkerStorage(id, latLng, distance){
		this.id = id;
		this.latLng = latLng;
		this.distance = distance;
		this.tasks = [];
	}

	MarkerStorage.prototype.addTask = function(task) {
  this.tasks.push(task)
};

	function initialize() {
		var mapOptions = {
			zoom: 18,
			center: new google.maps.LatLng(55.912856, -3.321567),
			mapTypeId: google.maps.MapTypeId.ROADMAP,
            disableDefaultUI: true,
		};

		poly = new google.maps.Polyline({
		  strokeColor: '#000000',
		  strokeOpacity: 1.0,
		  strokeWeight: 3
	  });

		map = new google.maps.Map(document.getElementById('google-map-default'), mapOptions);
		poly.setMap(map);
		map.addListener('click', addLatLng);
	}

	function addLatLng(event) {
	  var path = poly.getPath();

	  // Because path is an MVCArray, we can simply append a new coordinate
	  // and it will automatically appear.

	  path.push(event.latLng);

	  // Add a new marker at the new plotted point on the polyline.
	  var marker = new google.maps.Marker({
	    position: event.latLng,
	    title: '#' + path.getLength(),
	    map: map,
			draggable: false
	  });

		// Caclulate the distance travelled from the previous marker to this one.
		if(path.getLength() > 1){
			var previous_latlng = path.getAt(path.getLength() - 2);
			var distance = google.maps.geometry.spherical.computeDistanceBetween(previous_latlng, event.latLng).toFixed(2);
		}else{
			var distance = 0;
		}

		var contentwindow  = "Hello from " + path.getLength() + "<br>" +
											   "Distance: " + distance + "<br>" +
												 "Latitude: " + event.latLng.lat() + "<br>" +
												 "Longitude: " + event.latLng.lng() + "<br>" +
												 '<button type="button">Add Task</button>' +
												 '<button id="rm-' + path.getLength() + '" type="button">Remove Waypoint</button>';

		var infowindow = new google.maps.InfoWindow({
		      content: contentwindow
		  });


		google.maps.event.addListener(marker, 'click', function(){
       infowindow.open(map, marker);
     });

		 //Add all info to stuff array
		 var marker_store = new MarkerStorage(path.getLength(), event.latLng, distance);
		 marker_store.addTask(0);
 		stuff.push(marker_store);
		//document.forms[0].elements["waypoints"].value = stuff;
		document.getElementById("input-waypoints").value = getWaypoints();
	}
	google.maps.event.addDomListener(window, 'load', initialize);

	$(window).resize(function() {
        google.maps.event.trigger(map, "resize");
	});

	var defaultMapStyles = [];
    var flatMapStyles = [{"stylers":[{"visibility":"off"}]},{"featureType":"road","stylers":[{"visibility":"on"},{"color":"#ffffff"}]},{"featureType":"road.arterial","stylers":[{"visibility":"on"},{"color":"#fee379"}]},{"featureType":"road.highway","stylers":[{"visibility":"on"},{"color":"#fee379"}]},{"featureType":"landscape","stylers":[{"visibility":"on"},{"color":"#f3f4f4"}]},{"featureType":"water","stylers":[{"visibility":"on"},{"color":"#7fc8ed"}]},{},{"featureType":"road","elementType":"labels","stylers":[{"visibility":"off"}]},{"featureType":"poi.park","elementType":"geometry.fill","stylers":[{"visibility":"on"},{"color":"#83cead"}]},{"elementType":"labels","stylers":[{"visibility":"off"}]},{"featureType":"landscape.man_made","elementType":"geometry","stylers":[{"weight":0.9},{"visibility":"off"}]}];
    var turquoiseWaterStyles = [{"featureType":"landscape.natural","elementType":"geometry.fill","stylers":[{"visibility":"on"},{"color":"#e0efef"}]},{"featureType":"poi","elementType":"geometry.fill","stylers":[{"visibility":"on"},{"hue":"#1900ff"},{"color":"#c0e8e8"}]},{"featureType":"landscape.man_made","elementType":"geometry.fill"},{"featureType":"road","elementType":"geometry","stylers":[{"lightness":100},{"visibility":"simplified"}]},{"featureType":"road","elementType":"labels","stylers":[{"visibility":"off"}]},{"featureType":"water","stylers":[{"color":"#7dcdcd"}]},{"featureType":"transit.line","elementType":"geometry","stylers":[{"visibility":"on"},{"lightness":700}]}];
    var icyBlueStyles = [{"stylers":[{"hue":"#2c3e50"},{"saturation":250}]},{"featureType":"road","elementType":"geometry","stylers":[{"lightness":50},{"visibility":"simplified"}]},{"featureType":"road","elementType":"labels","stylers":[{"visibility":"off"}]}];
    var oldDryMudStyles = [{"featureType":"landscape","stylers":[{"hue":"#FFAD00"},{"saturation":50.2},{"lightness":-34.8},{"gamma":1}]},{"featureType":"road.highway","stylers":[{"hue":"#FFAD00"},{"saturation":-19.8},{"lightness":-1.8},{"gamma":1}]},{"featureType":"road.arterial","stylers":[{"hue":"#FFAD00"},{"saturation":72.4},{"lightness":-32.6},{"gamma":1}]},{"featureType":"road.local","stylers":[{"hue":"#FFAD00"},{"saturation":74.4},{"lightness":-18},{"gamma":1}]},{"featureType":"water","stylers":[{"hue":"#00FFA6"},{"saturation":-63.2},{"lightness":38},{"gamma":1}]},{"featureType":"poi","stylers":[{"hue":"#FFC300"},{"saturation":54.2},{"lightness":-14.4},{"gamma":1}]}];
    var cobaltStyles  = [{"featureType":"all","elementType":"all","stylers":[{"invert_lightness":true},{"saturation":10},{"lightness":10},{"gamma":0.8},{"hue":"#293036"}]},{"featureType":"water","stylers":[{"visibility":"on"},{"color":"#293036"}]}];
    var darkRedStyles   = [{"featureType":"all","elementType":"all","stylers":[{"invert_lightness":true},{"saturation":10},{"lightness":10},{"gamma":0.8},{"hue":"#000000"}]},{"featureType":"water","stylers":[{"visibility":"on"},{"color":"#293036"}]}];

	$('[data-map-theme]').click(function() {
        var targetTheme = $(this).attr('data-map-theme');
        var targetLi = $(this).closest('li');
        var targetText = $(this).text();
        var inverseContentMode = false;
        $('#map-theme-selection li').not(targetLi).removeClass('active');
        $('#map-theme-text').text(targetText);
        $(targetLi).addClass('active');
        switch(targetTheme) {
            case 'flat':
                map.setOptions({styles: flatMapStyles});
                break;
            case 'turquoise-water':
                mapfault.setOptions({styles: turquoiseWaterStyles});
                break;
            case 'icy-blue':
                map.setOptions({styles: icyBlueStyles});
                break;
            case 'cobalt':
                map.setOptions({styles: cobaltStyles});
                inverseContentMode = true;
                break;
            case 'old-dry-mud':
                map.setOptions({styles: oldDryMudStyles});
                break;
            case 'dark-red':
                map.setOptions({styles: darkRedStyles});
                inverseContentMode = true;
                break;
            default:
                map.setOptions({styles: defaultMapStyles});
                break;
        }

        if (inverseContentMode === true) {
            $('#content').addClass('content-inverse-mode');
        } else {
            $('#content').removeClass('content-inverse-mode');
        }
	});
};

var PlottingGoogleMap = function (mission_id) {
	"use strict";
    return {
        //main function
        init: function (mission_id) {
            handleGoogleMapSetting(mission_id);
        }
    };
}();
