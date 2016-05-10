/*
Template Name: Color Admin - Responsive Admin Dashboard Template build with Twitter Bootstrap 3.3.5
Version: 1.9.0
Author: Sean Ngu
Website: http://www.seantheme.com/color-admin-v1.9/admin/
*/
function process_task_request(form) {
	var form_data = $('form').serializeArray();
	var task_id = -1
	var platform_id = -1;
	// Extract form data
	for (i = 0; i < form_data.length; i++) {
		var ix = form_data[i]
		if(ix.name == "task" && ix.value != ''){
			task_id = ix.value;
		}else if (ix.name == "platform" && ix.value != ''){
			platform_id = ix.value;
		}
	}

	//Check we have all the data we need
	var failed = false;
	if(task_id == -1){
		alert("No task provided!");
		failed = true;
	}
	if (platform_id == -1){
		alert("No platform provided!");
		failed = true;
	}
	if (!failed){
		send_task_request("", task_id, platform_id);
	}

}

function send_task_request(ip_address, task_id, platform_id){
	send_ajax_post(
		'/missionplanner/send_task_request',
		{
			'command':'run_task',
			'ip_address':ip_address,
			'task': task_id,
			'platform':platform_id
		}
	);
}



var handleTaskButtons = function(ip_address) {

	"use strict";



};

var TaskRequests = function (ip_address) {
	"use strict";
    return {
        //main function
        init: function (ip_address) {
            handleTaskButtons(ip_address);
        }
    };
}();
