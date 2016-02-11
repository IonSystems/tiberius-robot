/*
Template Name: Color Admin - Responsive Admin Dashboard Template build with Twitter Bootstrap 3.3.5
Version: 1.9.0
Author: Sean Ngu
Website: http://www.seantheme.com/color-admin-v1.9/admin/
*/

function run_task(ip_address, task_id){
	$.ajax({
			url: '/control/send_task_request',
			type: 'POST',
			data: {
							'command':'run',
							'task_id':task_id,
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
