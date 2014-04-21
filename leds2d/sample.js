var image = new Image();  
image.src = "hs_appl1.png";  
//image.src = "p_blackm.png"

// http://doiop.com/

var zoom = 7;
var offsBase = {x:1, y:6}
var xoffs = offsBase.x;
var yoffs = offsBase.y;
var numbersDisp = 0; // 0:dec, 1:hex, 2:2^n

var xend = 0; 
var ystart = 0;
var labels = null;
var cpedit = null;
var intext = null;
var BITS_WIDTH = 224;
var BITS_HEIGHT = 16;

var MAP_WIDTH = BITS_WIDTH;
var MAP_HEIGHT = BITS_HEIGHT + 10;
var map = [];
var inHandPaint = false;
var BLACK = "rgba(0,0,0,255)", WHITE = "rgba(255,255,255,255)";

var urlarg = window.location.search.substring(1)


function initMap() {
	for(var i = 0; i < MAP_WIDTH; ++i) {
		map[i] = []
		for(var j = 0; j < MAP_HEIGHT; ++j) {
			map[i][j] = WHITE;
		}
	}
}
function copyMap(from) {
	to = []
	for(var i = 0; i < MAP_WIDTH; ++i) {
		to[i] = []
		for(var j = 0; j < MAP_HEIGHT; ++j) {
			to[i][j] = from[i][j];
		}
	}
	return to;
}
	
function drawGrid() 
{
	for (var x = 0; x <= BITS_WIDTH; ++x) {
		ctx.moveTo(x * zoom, 0);
		ctx.lineTo(x * zoom, canvas.height);	
	}
    
	for (var by = 0; by <= BITS_HEIGHT; ++by) {
		ctx.moveTo(0, (offsBase.y + by) * zoom );
		ctx.lineTo(xend, (offsBase.y + by) * zoom);	
	}
	ctx.strokeStyle = "rgba(170,170,170,255)";
	ctx.stroke();
	
	/*ctx.fillStyle = "rgb(0,0,0)";
	ctx.font=""+(zoom-1)+"px monospace";
	ctx.save();
	ctx.translate(xend, ystart);
	ctx.rotate(-Math.PI/2);
	t = 1;
	for(var i = 0; i < BITS_WIDTH; ++i) {
		if (numbersDisp == 0)
			s = "" + t.toLocaleString();
		else if (numbersDisp == 1)
			s = "0x" + t.toString(16);
		else if (numbersDisp == 2)
			s = "2^" + i;
		ctx.fillText(s, 4, -4 - zoom*i);
		t = t*2;
	}
	ctx.restore();*/
}	
	
function drawMap() {
	for(var y = 0; y < MAP_HEIGHT; ++y) {
		for(var x = 0; x < MAP_WIDTH; ++x) {
			ctx.fillStyle = map[x][y];
			ctx.fillRect(x * zoom, y * zoom, zoom, zoom);		
		}
	}
}

function initCoord() {
	xend = canvas.width;
	ystart = zoom * offsBase.y;
}
	
function draw(skipValues, skipCp) {	
	canvas.width = zoom * (MAP_WIDTH + 2);
	canvas.height = zoom * (MAP_HEIGHT)
	initCoord();
	drawMap();
	drawGrid();
	if (!skipValues)
		updateValues(skipCp);
}

var mouseStart = null;
var mapDragged = null;

var paintColor = BLACK

function handPaint(e, samp) {
	var x = Math.ceil((e.clientX-8) / zoom) - 1;
	var y = Math.ceil((e.clientY-8) / zoom) - 1;
    
	s = map[x][y]
	if (samp) {
		if (s == "rgba(255,255,255,255)")
			paintColor = BLACK
		else
			paintColor = WHITE;
	}
	map[x][y] = paintColor
	draw();
}

function mapToMap(from) {
	initMap();
	for (var x = 0; x < MAP_WIDTH; ++x){
		for (var y = 0; y < MAP_HEIGHT; ++y){
			var sx = xoffs + x, sy = yoffs + y;
			if (sx < 0 || sx >= MAP_WIDTH || sy < 0 || sy >= MAP_HEIGHT)
				continue;		
			map[x][y] = from[sx][sy]
		}
	}
}

function mouseDown(e) {
	mouseStart = {x:e.clientX, y:e.clientY};
	if (inHandPaint)
		handPaint(e, true)
	else
		mapDragged = copyMap(map)

}
function mouseUp(e) {
	mouseStart = null;
	mapDragged = null
}

function mouseMove(e) {
	if (mouseStart === null)
		return;
	if (inHandPaint) {
		handPaint(e)
		return
	}
	var x = Math.floor((mouseStart.x - e.clientX)/zoom);
	var y = Math.floor((mouseStart.y - e.clientY)/zoom);
	if (x == xoffs && y == yoffs) 
		return;
	xoffs = x;
	yoffs = y;	
	if (mapDragged)
		mapToMap(mapDragged);
	draw();
}

function pad(n, width, z) {
  z = z || '0';
  n = n + '';
  return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
}

function isDark(c) {
	c = parseInt(c.substr(5,3));
	return (c < 200)
}

function updateValues(skipCp) {
	if (labels === null)
		return;
	
	for(var x = 0; x < BITS_WIDTH; ++x) {
		var v = 0;
		bit = 1;
		for(var y = 0; y < BITS_HEIGHT; ++y) {
			var sx = x
			var sy = offsBase.y + y

			var c = map[sx][sy]
			if (isDark(c))
				v += bit
			bit = bit*2	
		}
		if (numbersDisp != 0 && v != 0)
			v = "0x" + pad(v.toString(16), 8)
		labels[x].value = v; //.toString(16);
	}
	if (!skipCp)
		updateCpValues()
}

// large text area at the bottom
function updateCpValues() {
	var v = ""
	for(var x = 0; x < BITS_WIDTH; ++x) {
		v += labels[x].value
		if (x < BITS_WIDTH - 1)
			v += ","
	}
	cpedit.value = v
}

function imageToMap(img) {
	initMap();
    imgData = img.data
	for (var x = 0; x < img.width; ++x){
		for (var y = 0; y < img.height; ++y){
			var sx = offsBase.x + x, sy = offsBase.y + y;
			if (sx < 0 || sx > MAP_WIDTH || sy < 0 || sy > MAP_HEIGHT)
				continue;			
			var i = (y * img.width + x)*4;
			var r = imgData[i  ];
			var g = imgData[i+1];
			var b = imgData[i+2];
			var a = imgData[i+3];
			map[sx][sy] = "rgba("+r+","+g+","+b+","+(a)+")";
		}
	}	
}

function loadImage() {
	var offtx = document.createElement('canvas').getContext('2d');
	offtx.drawImage(image,0,0);
	var img = offtx.getImageData(0, 0, image.width, image.height);
	imageToMap(img);
    draw()
}

$(image).load(function() {  
	if (urlarg == "") {
		loadImage();
	}
});  

function argToMap(arg) {
	var nums = arg.split(/[&,]/);
	for(var i = 0; i < nums.length; ++i) {
		setTextFor(i, nums[i])
	}
	updateCpValues();
}


function createElem(kind, type, value, x, y, click) {
    var i = document.createElement(kind);
    i.type = type;
	if (value !== null)
		i.value = value;
	i.style.position = "absolute"
	i.style.left = x + "px";
	i.style.top = y + "px";
    i.onclick = click;
    document.body.appendChild(i);
	return i;
}
function createInput(type, label, x, y, func) {
	return createElem("input", type, label, x, y, func);
}

function repos() {
	draw();
	cpedit.style.top = ystart + canvas.height + 20 + "px"
}

function setTextFor(i, s) {
	bit = 1;

	val = parseInt(s, (numbersDisp == 0)?10:16  )
	for(y = 0; y < BITS_HEIGHT; ++y) {
        var sy = y + offsBase.y
		//var dark = isDark(map[i][sy])
		if ( (val & bit) != 0) {
			//if (!dark)
			map[i][sy] = BLACK
		}
		else //if (dark)
			map[i][sy] = WHITE
		bit = bit * 2;
	}
}

function textChange(i, ed) {
	setTextFor(i, ed.value)
	draw(true)
	updateCpValues()
}

function cpEditInput() {
	var x = cpedit.value.split(",")
	for(var i = 0; i < labels.length; ++i) {
		if (i < x.length)
			setTextFor(i, x[i])
		else
			setTextFor(i, 0)
	}
	draw(false, true)
}

function makeURL() {
	var s = window.location.origin + window.location.pathname + "?" + cpedit.value;
	return s;
}

function sendBits() {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange=function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200)
        {
            //document.getElementById("myDiv").innerHTML = xmlhttp.responseText;
        }
    }
    xmlhttp.open("GET", "change_bits?" + cpedit.value, true);
    xmlhttp.send();
}

function dispTextChange() {
    function d() {
        ctx.fillStyle = "rgb(255,255,255)"
        ctx.fillRect(0,0,200,30)
        ctx.fillStyle = "rgb(0,0,0)";
        ctx.font="22px arial";
        ctx.textBaseline="top";  
        ctx.fillText(intext.value, 0, -4)
    }

    //ctx.translate(-0.5, 0);
    d()
    var imgd = ctx.getImageData(0, 0, 200, 16);
    imageToMap(imgd);
    draw()
    d()
    sendBits()

}


initMap();	

window.onload = function()
{
	//alert("X" + urlarg +"X")	
	initCoord();
    /*createInput("button", "numbers", xend + 20, 10, function(){
        numbersDisp = (numbersDisp + 1) % 3;
		draw();
    });*/
	labels = []
	for(var i = 0; i < BITS_WIDTH; ++i) {
		//var l = createInput("text", "0", xend + 20, ystart + 5 + i*zoom, null);
		//l.style.fontFamily = "monospace"
		labels[i] = { value:0 }
		//l.oninput = function(ii,ll) { return function() { textChange(ii, ll) } }(i,l)
	}
    widgetsx = 0
    widgetsy = 500
	createInput("button", "+", widgetsx + 20, widgetsy + 35, function(){
        zoom += 2;
		repos();
    });
	createInput("button", "-", widgetsx + 50, widgetsy + 35, function(){
        zoom -= 2;
		repos();
    });	
	
	var pnt = createInput("checkbox", false, widgetsx + 20, widgetsy + 60, function(){
		inHandPaint = !inHandPaint
    });	
	pnt.id = "paintCheckbox";
	var lbl = createElem("label", null, "Paint", widgetsx + 45, widgetsy + 60, null)
	lbl.htmlFor = "paintCheckbox"
	lbl.innerText = "Paint";
	
	createInput("button", "clear", widgetsx + 90, widgetsy + 10, function(){
        initMap()
		draw()
    });	
	
	createInput("button", "URL", widgetsx + 90, widgetsy + 70, function() {
		window.prompt("The URL:", makeURL());
	});
    createInput("button", "Send", widgetsx + 150, widgetsy + 70, function() {
		sendBits()
	});
    intext = createInput("text", "Hello World!", widgetsx + 20, widgetsy + 100, null);
    intext.oninput = dispTextChange
    

	var fload = createInput("file", null, widgetsx + 90, widgetsy + 35, null);
	fload.onchange = function() {
		var f = this.files[0]
		image.src = window.URL.createObjectURL(f)
		fload.value = null
	};
	
	cpedit = createElem("textarea", null, "0", 10, ystart + canvas.height + 20, null)
	cpedit.style.width = xend + "px"
	cpedit.style.height = "170px"
	cpedit.oninput = cpEditInput
	
	canvas.onmousedown = mouseDown;
	document.onmouseup = mouseUp;
	document.onmousemove = mouseMove;
	
    dispTextChange()
	if (urlarg != "") {
		argToMap(urlarg)
		draw()
	}
}


