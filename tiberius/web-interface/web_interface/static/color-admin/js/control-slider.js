
var handleControlSliders = function(ip_address) {

	"use strict";
  $("#speed_slider").ionRangeSlider({
      type: "single",
      min: 0,
      max: 100,
      from: 50,
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
}
var ControlSliders = function (ip_address) {
	"use strict";
    return {
        //main function
        init: function (ip_address) {
            handleControlSliders(ip_address);
        }
    };
}();
