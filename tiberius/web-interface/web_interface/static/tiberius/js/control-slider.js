
var handleControlSliders = function(ip_address, initial_speed) {

	"use strict";

  $("#speed_slider").ionRangeSlider({
      type: "single",
      min: 0,
      max: 100,
      from: initial_speed,
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
              data: {'speed':value, 'ip_address':ip_address},
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
var ControlSliders = function (ip_address) {
	"use strict";
    return {
        //main function
        init: function (ip_address, initial_speed) {
            handleControlSliders(ip_address, initial_speed);
        }
    };
}();
