
var cellData;
var cellPositionData;

var testZonesi = 3;
var testZonesj = 7;
//var testPath = [(1,2), (1,3), (2,3), (2,4), (2,5), (3,5)];
var testPath = [2,3,12,13, 22,23,24, 33];
var tempHeuristics = [];
var tempCosts = [];
var tempImg = [];


function setDirection(dir){
	cell.html(dir);
}

/*function getDirections(){
//for each cell which has a direction, calculate which one
	var tempDir = "";
	for (i = 0; i < rows; i++){
		for(j=0; j< cols; j++){
			//if i, j-1 has arrow not facing towards
			if(cell(){
				tempDir += "left";
			}
			//i, j+1 has arrow
			else if(){
				tempDir += "right";
			}
			//i-1, j has arrow
			else if(){
				tempDir += "up";
			}
			//i+1, j has arrow
			else (){
				tempDir += "down";
			}
			tempDir += "Img";
			cell.setDirection(tempDir);
		}
	}
}*/

function getCosts(rows){
	var temp = Math.floor((Math.random()*rows+1));
	return temp;
}

function getColours(Heuristic){
return (12 * Heuristic);
}

function createArray(length) {
    var arr = new Array(length || 0),
        i = length;

    if (arguments.length > 1) {
        var args = Array.prototype.slice.call(arguments, 1);
        while(i--) arr[length-1 - i] = createArray.apply(this, args);
    }
    return arr;
}

function addImage(i , j, rows){
for (a = 0; a < testPath.length; a++){
		if(testPath[a]== i*rows+j){
			cell.innerHTML = leftImg;
		}
	}
}

function checkPath(a, i, j, rows, cell, heuristic){
			cell.innerHTML = "<h1>(" + (rows-i-1) + ","+ (j-1) + ")<br></h1>";
			//cell.style.backgroundColor = "hsla(" + getColours(Math.random())+ ", 100%, 50%, 1)";
			cell.style.backgroundColor = "hsla(" + getColours(9-heuristic) + ", 100%, 50%, 1)";
			cell.style.border = "2px solid black";
			//cell.style.textAlign = "left";
			//cell.style.verticalAlign = "top";
}

function createCell(row, i, j, rows, cols, heuristic){
	var cell = row.insertCell(j);
	//check if cell is in the path and if so add in a directional arrow
	if (i == Math.floor(rows/2) && j == Math.floor(cols/2)+1){
		cell.innerHTML = tiberiusImg;
		cell.style.backgroundColor = "white";
	}
	else if ( i == rows && j == 0){
		cell.innerHTML = "";
		cell.style.backgroundColor = "white";
		cell.style.border = "thin solid white";
	}
	else if(i == rows){
		cell.innerHTML = ""+(j-1);
		cell.style.backgroundColor = "white";
		cell.style.border = "thin solid white";
	}
	else if(j == 0){
		cell.innerHTML = ""+(rows - i-1);
		cell.style.backgroundColor = "white";
		cell.style.border = "thin solid white";
	}
	else{
		for (a = 0; a < testPath.length; a++){
			checkPath(a, i, j , rows, cell, heuristic);
		}
	}
	return cell;
}

function sortDirections(){

}

function getLatLong(i, j){
//Need to get real lat and long values from database
	var latLong = [];
	latLong.push((Math.random()*360).toFixed(5));
	latLong.push((Math.random()*100).toFixed(5));
	return latLong;
}

function showLongLat(row, col, cell){
	if(col > 0&& row < 9){
		cell.html("<h1> Lat.: " + cellData[row][col][0] + "<br></h1>"+
		"<h1> Long.: " + cellData[row][col][1] + "<br></h1>");
		}
}

function hideLongLat(row, col, cell){
	if(row < 9 && col > 0){
		var temp = ((+row *10)+ +col);
		if((row == 4 && col == 5) ){
				cell.html(cellPositionData[row][col]);
		}
		else {
			cell.html(cellPositionData[row][col] + "<h2>" + tempCosts[temp] + "</h2>");
		}
	}
}

function createGrid(name, rows, cols, data, heuristic) {
	cellData = createArray(rows,cols,heuristic);
	cellPositionData = createArray(rows,cols);
    var table = document.getElementById(name);
	var lat, lon, temp;
	for (i = 0; i < rows+1; i++){
		var row = table.insertRow(i);
		for (j=0; j < cols+1; j++){
			//temporary version of heuristic
			temp = getCosts(rows);
			tempCosts.push(temp);
			tempImg.push(addImage(i, j, rows));
			addImage(i,j,rows);
			cell = createCell(row, i, j, rows, cols, temp);
			if(i < rows && j > 0){
				latLong = getLatLong(i,j);
				cellData[i][j] = latLong;
				cellPositionData[i][j] = cell.innerHTML;
				if(!(i == Math.floor(rows/2) && j == Math.floor(cols/2)+1)){
					cell.innerHTML += "<h2>"+temp+"</h2>";
				}
			}
			cell.id = i + "," + j;
		}
	}
}

createGrid("table", 9, 9, "data", 1)

$(function(){
    $("#table tr td").mouseenter(function(event) {
		var position = $(this).attr('id').split(",");
		var row = position[0];
		var col = position[1];
        showLongLat(row, col, $(this));
    });
});

$(function(){
    $("#table tr td").mouseleave(function(event) {
		var position = $(this).attr('id').split(",");
		var row = position[0];
		var col = position[1];
        hideLongLat(row, col, $(this));
    });
});
