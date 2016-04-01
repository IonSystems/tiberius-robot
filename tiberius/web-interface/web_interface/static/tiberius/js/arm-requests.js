/*
Template Name: Color Admin - Responsive Admin Dashboard Template build with Twitter Bootstrap 3.3.5
Version: 1.9.0
Author: Sean Ngu
Website: http://www.seantheme.com/color-admin-v1.9/admin/
*/

function send_command(ip_address, command_name, command_value){
	$.ajax({
			url: '../send_arm_request',
			type: 'POST',
			data: {command_name:command_value, 'ip_address':ip_address},
			success: function (result) {
				//alert("anything");
			},
			error: function(error_msg){
				alert(error_msg);
			}
	});
}

function arm_unavailable(){
	// Disable arm positioning buttons
	document.getElementById("arm_button_x_minus").disabled = true;
	document.getElementById("arm_button_y_plus").disabled = true;
	document.getElementById("arm_button_y_minus").disabled = true;
	document.getElementById("arm_button_x_plus").disabled = true;
	document.getElementById("arm_button_stop").disabled = true;
	document.getElementById("arm_button_z_plus").disabled = true;
	document.getElementById("arm_button_z_minus").disabled = true;

	// Disable claw grasping buttons
	document.getElementById("arm_button_grab_minus").disabled = true;
	document.getElementById("arm_button_grab_plus").disabled = true;

	// Disable complex command buttons
	document.getElementById("arm_button_centre").disabled = true;
	document.getElementById("arm_button_basket").disabled = true;
	document.getElementById("arm_button_park").disabled = true;

}

var handleArmButtons = function(ip_address, initial_values) {
	"use strict";

	// Convert initial values into JSON
	initial_values = JSON.parse(initial_values);

	var x_pos = initial_values['x'];
	var y_pos = initial_values['y'];
	var z_pos = initial_values['z'];

	// If we don't get valid initial positions, disable arm buttons.
	if(!x_pos){
		arm_unavailable();
	}

  $('#arm_button_x_minus').click(function() {
		x_pos = x_pos - 20;
		send_command(ip_address, 'arm_button_x', x_pos);
  });
	$('#arm_button_y_plus').click(function() {
		y_pos = y_pos + 20;
		send_command(ip_address, 'arm_button_y', y_pos);
  });
	$('#arm_button_y_minus').click(function() {
		y_pos = y_pos - 20;
		send_command(ip_address, 'arm_button_y', y_pos);
  });
	$('#arm_button_x_plus').click(function() {
		x_pos = x_pos + 20;
		send_command(ip_address, 'arm_button_x', x_pos);
  });
	$('#arm_button_stop').click(function() {
		send_command(ip_address, 'stop', 'True');
  });
	$('#arm_button_z_plus').click(function() {
		z_pos = z_pos + 20;
		send_command(ip_address, 'arm_button_z', z_pos);
  });
	$('#arm_button_z_minus').click(function() {
		z_pos = z_pos + 20;
		send_command(ip_address, 'arm_button_z', z_pos);
  });
};

var ArmRequests = function (ip_address, initial_values) {
	"use strict";
    return {
        //main function
        init: function (ip_address, initial_values) {
            handleArmButtons(ip_address, initial_values);
        }
    };
}();
