//------------------------------------------------------------------------------
// Project:	Polyhedra
// Copyright:	Copyright (C) 1994-2012 by ENEA Software AB.
//		All Rights Reserved
// Description:	Javascript for the Polyhedra Websocket example.
//------------------------------------------------------------------------------

// Port of websocket server. The hostname will be constructed later.
var websocketPort = "3400"

// Full URL of websocket server
var wsUri;

// Log all received messages.
var logging=true;

// HTML table for display of currencies.
var currencyTable;


// HTML table for display of websocket messages received.
var logTable;

// HTML button to control logging.
var loggingButton;

// Websocket endpoint.
var websocket;

function init()
{
    // Find components of interest in web page.
    loggingButton = document.getElementById("loggingButton");
    logTable = document.getElementById("logTable");
    currencyTable = document.getElementById("currencyTable");

    // The websocket should be on the host that the web page came from.
    var hostname = window.location.hostname;
    if(hostname == "")
    {
	// If the page was loaded directly, assume the websocket client is
	// on this machine.
	hostname = "localhost";
    }
    wsUri = "ws://" + hostname + ":" + websocketPort

    // Create websocket endpoint.
    setupCurrencyWebSocket();
}

function setupCurrencyWebSocket()
{
    // The WebSocket protocol is accessed differently on FireFox.
    if(window.WebSocket)
    {
	websocket = new WebSocket(wsUri);
    }
    else if(window.MozWebSocket)
    {
	websocket = new MozWebSocket(wsUri);
    }
    else
    {
	alert("WebSocket is not supported in this browser");
    }

    // Handlers for events on the web socket.
    websocket.onopen = function(evt) { onOpen(evt) };
    websocket.onclose = function(evt) { onClose(evt) };
    websocket.onmessage = function(evt) { onMessage(evt) };
    websocket.onerror = function(evt) { onError(evt) };
 }

function onOpen(evt)
{
    writeToLog("CONNECTED");

    // This is an example request. Extend websocket.c to understand more request types.
    doSend("currency");
}

function onClose(evt)
{
    writeToLog("DISCONNECTED");
}

function onMessage(evt)
{
    writeToLog("RECEIVED: " + evt.data);

    // The received message is assumed to be JSON formatted.
    // In a production application, replace with a secure JSON evaluation library.
    // This line could execute arbitrary code from an untrusted server.
    msg = eval('(' + evt.data + ')');

    // Process message depending on its type.
    switch(msg.type)
    {
    case 'initial':
    case 'insert':
	addRow(msg.code,msg.country,msg.name,msg.usdollar);
	break;

    case 'update':
	updateRow(msg.code,msg.country,msg.name,msg.usdollar);
	break;

    case 'delete':
	deleteRow(msg.code);
	break;

    }
 }

function onError(evt)
{
    writeToLog('<span style="color: red;">ERROR:</span> ' + evt);
}

function doSend(message)
{
    // Send message to the server.
    writeToLog("SENT: " + message);
    websocket.send(message);
}

function writeToLog(message)
{
    /* If logging is enabled, add to the log */
    if(logging==true)
    {
	var currentTime = new Date()
	var hours = currentTime.getHours()
	var minutes = currentTime.getMinutes()
	var seconds = currentTime.getSeconds()
	if (hours < 10)
	    hours = "0" + hours
	if (minutes < 10)
	    minutes = "0" + minutes
	if (seconds < 10)
	    seconds = "0" + seconds

	var row = logTable.insertRow(logTable.rows.length);
	var cell = row.insertCell(0);
	cell.innerHTML = '<span style="color: blue;">' + hours + ":" + minutes + ":" + seconds + "</span> "  + message;
	cell.className = "fixed";
	/* Limit log size */
	while(logTable.rows.length > 20)
	{
	    logTable.deleteRow(0);
	}
    }
}

function addRow(code,country,name,usdollar)
{
    // Add a new row to the end of the currency table.
    var rowCount = currencyTable.rows.length;
    var row = currencyTable.insertRow(rowCount);

    var cellCode = row.insertCell(0);
    cellCode.innerHTML = code;
    var cellCountry = row.insertCell(1);
    cellCountry.innerHTML = country;
    var cellName = row.insertCell(2);
    cellName.innerHTML = name;
    var cellUsdollar = row.insertCell(3);
    cellUsdollar.innerHTML = usdollar;
    cellUsdollar.className = "usdollar";
    var cellChange = row.insertCell(4);
    cellChange.innerHTML = "0";
    cellChange.className = "usdollar";
}

function updateRow(code,country,name,usdollar)
{
    // Find an existing row in the table by the country code.
    // replace the row's values with new data.
    try
    {
        var rowCount = currencyTable.rows.length;

        for(var i=0; i<rowCount; i++)
	{
            var row = currencyTable.rows[i];
            var cellCode = row.cells[0];
            if(code == cellCode.innerHTML)
	    {
		var cellCountry = row.cells[1];
		cellCountry.innerHTML = country;
		var cellName = row.cells[2];
		cellName.innerHTML = name;
		var cellUsdollar = row.cells[3];
		var oldVal = parseFloat(cellUsdollar.innerHTML);
		cellUsdollar.innerHTML = usdollar;
		var newVal = parseFloat(usdollar);

		// Alter the fields colour depending on the change in value.
		var colour = currencyTable.style.color;
		var change = (newVal - oldVal).toFixed(2);
		if(change > 0) 
		{
		    colour = '#009900'; // Green
		    change = "+" + change;
		}
		else if(change < 0)
		{
		    colour = '#990000'; // Red
		}
		var cellChange = row.cells[4];
		cellChange.innerHTML = change;
		cellChange.style.color = colour;
		cellChange.style.fontWeight = "bold";
		break;
            }
	}
    }catch(e)
    {
        alert(e);
    }
}

function deleteRow(code)
{
    // Find a row by the code column and delete that row.
    try
    {
        var rowCount = currencyTable.rows.length;

        for(var i=0; i<rowCount; i++) {
            var row = currencyTable.rows[i];
            var cellCode = row.cells[0];
            if(code == cellCode.innerHTML) {
                currencyTable.deleteRow(i);
                rowCount--;
                i--;
            }
        }
    }catch(e)
    {
        alert(e);
    }
}

function clearLog()
{
    // Tidy up the message log.
    // Triggered from the "Clear Log" button.
    while(logTable.rows.length > 0)
    {
	logTable.deleteRow(0);
    }
}
function toggleLogging()
{
    // Triggered from the "Enable/Disable Logging" button.
    var label = "Disable Logging"
    if(logging)
    {
	label = "Enable Logging";
    }
    loggingButton.value = label;
    logging = !logging;
}

// Only start once the page is fully loaded.
window.addEventListener("load", init, false);

//------------------------------------------------------------------------------
//------------------------------------------------------------------------------
