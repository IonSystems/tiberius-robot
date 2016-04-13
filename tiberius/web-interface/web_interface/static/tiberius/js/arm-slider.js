
var handleArmControlSliders = function(ip_address, initial_arm_speed) {

	"use strict";

  $("#arm_speed_slider").ionRangeSlider({
      type: "single",
      min: 0,
      max: 100,
      from: initial_arm_speed,
      onStart: function (data) {
          console.log("onStart");
      },
      onChange: function (data) {
          console.log("onChange");
      },
      onFinish: function (data) {
        var value = data.fromNumber;
          $.ajax({
              url: '../send_control_request',
              type: 'POST',
              data: {'arm_speed':value, 'ip_address':ip_address},
              success: function (result) {
              }
          });
      },
      onUpdate: function (data) {
          console.log("onUpdate");
      }
  });

	function getTiberiusSpeed(speed){
		alert(slider);
		slider.from = speed;
	}
}
var ArmControlSliders = function (ip_address, initial_arm_speed) {
	"use strict";
    return {
        //main function
        init: function (ip_address, initial_arm_speed) {
            handleArmControlSliders(ip_address, initial_arm_speed);
        }
    };
}();
