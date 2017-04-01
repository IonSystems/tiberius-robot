function set_buttons(disabled){
  var val = disabled = true ? 'disabled' : 'enabled';
  document.getElementById("button_forward").disabled = val;
  document.getElementById("button_backward").disabled = val;
  document.getElementById("button_right").disabled = val;
  document.getElementById("button_left").disabled = val;
  document.getElementById("button_stop").disabled = val;
}
