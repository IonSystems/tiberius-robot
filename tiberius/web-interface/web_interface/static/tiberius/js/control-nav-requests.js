/*
Template Name: Color Admin - Responsive Admin Dashboard Template build with Twitter Bootstrap 3.3.5
Version: 1.9.0
Author: Sean Ngu
Website: http://www.seantheme.com/color-admin-v1.9/admin/
*/


function send_waypoint_request(ip_address, latitude, longitude, speed){
	send_ajax_post(
		'/missionplanner/send_nav_request',
		{
			'command':'goto_waypoint',
			'ip_address':ip_address,
			'latitude': latitude,
			'longitude':longitude,
			'speed':speed
		}
	);
}

var handleNavigationButtons = function(ip_address) {

	"use strict";
	// When goto button is pressed, send a request to Tiberius to go to a waypoint.
	$(document).on("click", "#goto_button", function () {

      var latitude  = parseFloat($(this).data('latitude'));
			var longitude = parseFloat($(this).data('longitude'));
			var button_ip_address = $(this).data('ipaddress');
			var speed = $(this).data('speed');
			send_waypoint_request(ip_address, latitude, longitude, speed)
    //  $(".modal-body #bookId").val( myBookId );
		alert("button clicked. Lat: " + latitude + ", Long: " + longitude + ", ip: " + button_ip_address);
     // As pointed out in comments,
     // it is superfluous to have to manually call the modal.
     // $('#addBookDialog').modal('show');
});



};

var NavigationRequests = function (ip_address) {
	"use strict";
    return {
        //main function
        init: function (ip_address) {
            handleNavigationButtons(ip_address);
        }
    };
}();
