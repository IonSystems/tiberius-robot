function check_api_error(response){
	return !response.includes("error");
}

function check_online(response){
  return !response.includes("Error");
}

function check_response(response){
  if (!check_api_error(response)){
    alert("Error on Tiberius's API!");
  }else if(!check_online(response)){
    alert("Tiberius is offline!");
  };
}

function check_state(request, response){
	var requested = Object.keys(request)[0];
	if (requested == 'speed'){
		var req_speed = request['speed'];
		var resp_speed = JSON.parse(response)['speed'];
		if (req_speed != resp_speed){
			alert("The requested speed of " + req_speed + "could not be reached.");
		}
	}else{
		var responded = JSON.parse(response)['state'];
		if(requested != responded){
			alert("Command " + requested + " could not be completed.");
		}
	};
}

function send_ajax_post(url, data){
	$.ajax({
			url: url,
			type: 'POST',
			data: data,
			success: function (result) {
				check_response(result);
				check_state(data, result);
			},
			error: function(error_msg){
				alert(error_msg);
			}
	});
}
