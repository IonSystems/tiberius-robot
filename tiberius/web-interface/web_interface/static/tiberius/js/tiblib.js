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
