function charify(index){
  var labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  return labels[index % labels.length];
}
