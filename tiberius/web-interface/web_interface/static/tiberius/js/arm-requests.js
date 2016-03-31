/*
Template Name: Color Admin - Responsive Admin Dashboard Template build with Twitter Bootstrap 3.3.5
Version: 1.9.0
Author: Sean Ngu
Website: http://www.seantheme.com/color-admin-v1.9/admin/
*/

//Keyboard Listener
window.onkeydown = function (e) {
	var code = e.keyCode ? e.keyCode : e.which;
	if (code === 87) { //up key
			alert('up');
	} else if (code === 83) { //down key
			alert('down');
	} else if (code === 65) { //left key
			alert('left');
	} else if (code === 68) { //right key
			alert('right');
	}
};

function send_stop(ip_address){
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
}

var handleArmButtons = function(ip_address) {

	"use strict";
  $('#button_stop').click(function() {
    send_stop(ip_address);

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

var ArmRequests = function (ip_address) {
	"use strict";
    return {
        //main function
        init: function (ip_address) {
            handleArmButtons(ip_address);
        }
    };
}();
