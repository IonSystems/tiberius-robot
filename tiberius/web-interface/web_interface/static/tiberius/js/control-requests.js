/*
Template Name: Color Admin - Responsive Admin Dashboard Template build with Twitter Bootstrap 3.3.5
Version: 1.9.0
Author: Sean Ngu
Website: http://www.seantheme.com/color-admin-v1.9/admin/
*/




function send_stop(ip_address){
	$.ajax({
			url: '../send_control_request',
			type: 'POST',
			data: {'stop':true, 'ip_address':ip_address},
			success: function (result) {
				check_response(result);
			},
			error: function(error_msg){
				alert(error_msg);
			}
	});
}

function send_forward(ip_address){
	$.ajax({
			url: '../send_control_request',
			type: 'POST',
			data: {'forward':50, 'ip_address':ip_address},
			success: function (result) {
				check_response(result);
			},
			error: function(error_msg){
				alert(error_msg);
			}
	});
}

function send_backward(ip_address){
	$.ajax({
			url: '../send_control_request',
			type: 'POST',
			data: {'backward':50, 'ip_address':ip_address},
			success: function (result) {
				check_response(result);
			},
			error: function(error_msg){
				alert(error_msg);
			}
		});
}

function send_left(ip_address){
	$.ajax({
			url: '../send_control_request',
			type: 'POST',
			data: {'left':50, 'ip_address':ip_address},
			success: function (result) {
				check_response(result);
			},
			error: function(error_msg){
				alert(error_msg);
			}
	});
}

function send_right(ip_address){
	$.ajax({
			url: '../send_control_request',
			type: 'POST',
			data: {'right':50, 'ip_address':ip_address},
			success: function (result) {
				check_response(result);
			},
			error: function(error_msg){
				alert(error_msg);
			}
	});
}

var handleControlButtons = function(ip_address) {

	"use strict";

	//Keyboard Listener
	window.onkeydown = function (e) {
		var code = e.keyCode ? e.keyCode : e.which;
		if (code === 87) { //up key
				send_forward(ip_address);
		} else if (code === 83) { //down key
				send_backward(ip_address);
		} else if (code === 65) { //left key
				send_left(ip_address);
		} else if (code === 68) { //right key
				send_right(ip_address);
		} else if (code === 32) { //space bar
				send_stop(ip_address);
		}
	};


  $('#button_stop').click(function() {
    send_stop(ip_address);
  });
  $('#button_forward').click(function() {
    send_forward(ip_address);

  });
  $('#button_backward').click(function() {
    send_backward(ip_address);
  });
	$('#button_left').click(function() {
    send_left(ip_address);

  });
	$('#button_right').click(function() {
    send_right(ip_address);

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
