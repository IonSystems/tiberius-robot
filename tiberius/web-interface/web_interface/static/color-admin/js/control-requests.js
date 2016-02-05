/*
Template Name: Color Admin - Responsive Admin Dashboard Template build with Twitter Bootstrap 3.3.5
Version: 1.9.0
Author: Sean Ngu
Website: http://www.seantheme.com/color-admin-v1.9/admin/
*/

var handleControlButtons = function(ip_address) {

	"use strict";
  $('#button_stop').click(function() {
    $.ajax({
        url: '../send_control_request',
        type: 'POST',
        data: {'stop':true, 'ip_address':ip_address},
        success: function (result) {
          //alert("anything");
        },
				error: function(error_msg){
					alert(error_msg);
				}
    });

  });
  $('#button_forward').click(function() {
    $.ajax({
        url: '../send_control_request',
        type: 'POST',
        data: {'forward':50, 'ip_address':ip_address},
        success: function (result) {
          //alert("anything");
        },
				error: function(error_msg){
					alert(error_msg);
				}
    });

  });
  $('#button_backward').click(function() {
    $.ajax({
        url: '../send_control_request',
        type: 'POST',
        data: {'backward':50, 'ip_address':ip_address},
        success: function (result) {
          //alert("anything");
        },
				error: function(error_msg){
					alert(error_msg);
				}
    });

  });
	$('#button_left').click(function() {
    $.ajax({
        url: '../send_control_request',
        type: 'POST',
        data: {'left':50, 'ip_address':ip_address},
        success: function (result) {
          //alert("anything");
        },
				error: function(error_msg){
					alert(error_msg);
				}
    });

  });
	$('#button_right').click(function() {
    $.ajax({
        url: '../send_control_request',
        type: 'POST',
        data: {'right':50, 'ip_address':ip_address},
        success: function (result) {
          //alert("anything");
        },
				error: function(error_msg){
					alert(error_msg);
				}
    });

  });
};

var ControlRequests = function (ip_address) {
	"use strict";
    return {
        //main function
        init: function (ip_address) {
            handleControlButtons(ip_address);
        }
    };
}();
