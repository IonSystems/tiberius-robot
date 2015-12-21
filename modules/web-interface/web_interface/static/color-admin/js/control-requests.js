/*
Template Name: Color Admin - Responsive Admin Dashboard Template build with Twitter Bootstrap 3.3.5
Version: 1.9.0
Author: Sean Ngu
Website: http://www.seantheme.com/color-admin-v1.9/admin/
*/

var handleControlButtons = function() {

	"use strict";
  $('#button_stop').click(function() {
    $.ajax({
        url: 'send_control_request',
        type: 'POST',
        data: {'stop':true}, // An object with the key 'submit' and value 'true;
        success: function (result) {
          //alert("anything");
        }
    });

  });
  $('#button_forward').click(function() {
    $.ajax({
        url: 'send_control_request',
        type: 'POST',
        data: {'forward':50}, // An object with the key 'submit' and value 'true;
        success: function (result) {
          //alert("anything");
        }
    });

  });
  $('#button_backward').click(function() {
    $.ajax({
        url: 'send_control_request',
        type: 'POST',
        data: {'backward':50}, // An object with the key 'submit' and value 'true;
        success: function (result) {
          //alert("anything");
        }
    });

  });
};

var ControlRequests = function () {
	"use strict";
    return {
        //main function
        init: function () {
            handleControlButtons();
        }
    };
}();
