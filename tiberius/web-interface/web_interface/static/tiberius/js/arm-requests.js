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
			data: {
				'command_name':command_name,
				'command_value':command_value,
				'ip_address':ip_address
			},
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

	// Remove the unicode specifiers
	initial_values = initial_values.split('u').join('');
	// Replace the asterisks
	initial_values = initial_values.split("'").join('"');
	initial_values = JSON.parse(initial_values);

	var x_pos = initial_values['x'];
	var y_pos = initial_values['y'];
	var z_pos = initial_values['z'];
	var d = 10;
	// If we don't get valid initial positions, disable arm buttons.
	if(!x_pos){
		arm_unavailable();
	}

	// Buttons to change positions by d
  $('#arm_button_x_minus').click(function() {
		send_command(ip_address, 'arm_dx', -d);
  });
	$('#arm_button_y_plus').click(function() {
		send_command(ip_address, 'arm_dy', d);
  });
	$('#arm_button_y_minus').click(function() {
		send_command(ip_address, 'arm_dy', -d);
  });
	$('#arm_button_x_plus').click(function() {
		send_command(ip_address, 'arm_dx', d);
  });
	$('#arm_button_stop').click(function() {
		send_command(ip_address, 'stop', 'True');
  });
	$('#arm_button_z_plus').click(function() {
		send_command(ip_address, 'arm_dz', d);
  });
	$('#arm_button_z_minus').click(function() {
		send_command(ip_address, 'arm_dz', -d);
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
