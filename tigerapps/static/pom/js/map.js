//MAP: Sets up all functionality related to events triggered by interactions
//with the map, including map scroll + tile/building loading, building
//click, and zoom (future)

//EVENTS: Sets up all functionality related to making ajax calls to the
//server for filtering events + loading events in the info box
//NOTE: should be loaded before map.js

jmap = {};
jevent = {};
function mapInit() {
	//links
	jmap.tilesDir = '/static/pom/img/tiles/';
	jmap.bldgsDir = '/static/pom/img/bldgs/';
	jmap.bldgsFile = '/static/pom/js/bldgs.json';
	jmap.bldgsDefaultSrc = '.png';
	jmap.bldgsHoverSrc = '-h.png';
	jmap.bldgsEventSrc = '-e.png';
	jmap.bldgsEventHoverSrc = '-eh.png';
	
	//static references
	jmap.mapContainer = document.getElementById('jmap-container');
	jmap.map = document.getElementById('jmap-movable');
	jmap.info = document.getElementById('jmap-info');
	jmap.infoTop = document.getElementById('info-top');
	
	//static constants
	jmap.tileSZ = 256; //square
	//jmap.mapBounds = {x1:68,y1:55,x2:2816,y2:2048};
	jmap.mapBounds = {x1:77,y1:57,x2:2715,y2:2046};
	
	//for dragging
	jmap.mouseStart = null;
	jmap.mapStart   = null;
	jmap.objId		= null;

	//variables for loading tiles and buildings
	jmap.zoom = 4; 			//0=out,4=in
	var start = mapCenterToDisp(1380,620);
	jmap.dispX = start.x;	//displacement from the top-left
	jmap.dispY = start.y;
	jmap.map.style.left = -jmap.dispX;
	jmap.map.style.top = -jmap.dispY;
	
	loadBldgsJSON();
	jmap.loadedTiles = {};
	jmap.loadedBldgs = {};		  //{domEle,event:t/f}.. event is list of highlighted bldgs
	jevent.bldgCodeHasEvent = {}; //list of bldgs with events, according to Django
	jmap.mapLoading = false;

	//now setup the drag
	setupGlobalDrag();
	
	/***/
	
	//links
	jevent.urlFilteredBldgs = '/filtered/bldgs/';
	jevent.urlFilteredDataBldg = '/filtered/data/bldg/';
	jevent.urlFilteredDataAll = '/filtered/data/all/';
	
	jevent.htmlLoading = '<div class="info-bot-loading">&nbsp;Loading...' +
        '<img src="/static/shared/img/loading-spinner.gif" class="loading-spinner"></div>';

	//cache display-related tabs
	jevent.activeLayer = -1; //events=0, hours=1, menus=2, laundry=3, printers=4
	jevent.activeBldg = null;
}


/***************************************/
/* General conversion tools */
/***************************************/

//ensures x,y input are within the bounds of the map
function boundDispX(x) {
	return -Math.max(Math.min(x, -jmap.mapBounds.x1), jmap.mapContainer.offsetWidth-jmap.mapBounds.x2);
}
function boundDispY(y) {
	return -Math.max(Math.min(y, -jmap.mapBounds.y1), jmap.mapContainer.offsetHeight-jmap.mapBounds.y2);
}

//given a center coordinate, compute top-left coordinate (dispX/dispY)
function mapCenterToDisp(x,y) {
	return {
		x:boundDispX(jmap.mapContainer.offsetWidth/2-x),
		y:boundDispY(jmap.mapContainer.offsetHeight/2-y)
	};
}

//convert between tile index and HTML-id
function tileIndexToId(x,y) {
	return jmap.zoom+"-"+x+"-"+y;
}
function tileIdToIndex(id)  {
	var a=id.split('-');
	return {x:parseInt(a[1]),y:parseInt(a[2])};
}

//compute position of tile
function tileIdToPos(id) {
	var index = tileIdToIndex(id);
	return {
		left: index.x*jmap.tileSZ,
		top: index.y*jmap.tileSZ
	};
}

function bldgIdToCode(id) {
	return id.split("-")[1];
}
function bldgCodeToId(bldgCode) {
	return jmap.zoom+"-"+bldgCode;
}

//building position is 1:1 in zoom level 4
//function objIndexToPos(index) {}


/***************************************/
/* For drag-scroll function of the map */
/* http://www.webreference.com/programming/javascript/mk/column2/index.html */
/***************************************/

// bind drag-setup to mousedown on the elements
// bind mouseover->drag to mousemove anywhere, if drag-setup
// bind drag-unsetup to mouseup anywhere
function setupGlobalDrag() {
	document.onmouseup = recordMouseUp
	
	/* For getting building coordinates using mouse on map
	$(window).keydown(function(event) {
		if (event.ctrlKey && event.keyCode == 49) {
			event.preventDefault();
			$('#box3').val($('#box1').val());
			$('#box4').val($('#box2').val());
			$('#box7').val($('#box5').val()-$('#box3').val());
			$('#box8').val($('#box6').val()-$('#box4').val());
		}
		if (event.ctrlKey && event.keyCode == 50) {
			event.preventDefault();
			$('#box5').val($('#box1').val());
			$('#box6').val($('#box2').val());
			$('#box7').val($('#box5').val()-$('#box3').val());
			$('#box8').val($('#box6').val()-$('#box4').val());
		}
	})
	*/
}
function setupTileDrag(domEle) {
	domEle.onmousedown = function(ev){recordMouseDown(ev, jmap.map);};
	domEle.ondragstart = function(ev){ev.preventDefault();};
}

// records where the mouse click-down happened
function recordMouseDown(ev, domEle) {
	document.onmousemove = mouseMove;
	document.body.className = 'jmap-grabbing';
	jmap.mouseStart = mouseCoords(ev);
	var mapOffset = $(domEle).offset();
	var mapContainerOffset = $('#jmap-container').offset();
	jmap.mapStart = {x:mapOffset.left-mapContainerOffset.left, y:mapOffset.top-mapContainerOffset.top};
}
// erases that junk
function recordMouseUp() {
	document.onmousemove = null;
	document.body.className = '';
	jmap.mouseStart = null;
	jmap.mapStart   = null;
	loadTiles();
}
// Moves the map if mouse is clicked down on the map
function mouseMove(ev){
    // find the mouse position
    ev           = ev || window.event;
    var mousePos = mouseCoords(ev);
    
    // move the map to the correct position
    var diffX = mousePos.x - jmap.mouseStart.x;
    var diffY = mousePos.y - jmap.mouseStart.y;
    jmap.dispX = boundDispX(jmap.mapStart.x+diffX);
    jmap.dispY = boundDispY(jmap.mapStart.y+diffY);
    jmap.map.style.left = -jmap.dispX;
    jmap.map.style.top  = -jmap.dispY;

    //it's actually noticeably slower if we load for every drag
    //loadTiles();

	/* For getting building coordinates using mouse on map
	var c = mouseCoords(ev);
	var mapContainerOffset = $('#jmap-container').offset();
	$('#box1').val(jmap.dispX+c.x+mapContainerOffset.left);
	$('#box2').val(jmap.dispY+c.y+mapContainerOffset.top);
	*/
}

//Returns the current coordinates of the mouse
function mouseCoords(ev){
	if(ev.pageX || ev.pageY)
		return {x:ev.pageX, y:ev.pageY};
	return {
		x:ev.clientX+document.body.scrollLeft-document.body.clientLeft,
		y:ev.clientY+document.body.scrollTop-document.body.clientTop
	};	
}



/***************************************/
/* For tile loading function of map */
/***************************************/

// load and set up drag for tiles that are on the current view screen
function loadTiles() {
	var tileBounds = tilesOnMap();
	//alert(tileBounds.minX+','+tileBounds.maxX+';'+tileBounds.minY+','+tileBounds.maxY);
	for (x=tileBounds.minX; x<=tileBounds.maxX; x++) {
		for (y=tileBounds.minY; y<=tileBounds.maxY; y++) {
			var id = tileIndexToId(x,y);
			if (jmap.loadedTiles[id] == undefined) {
				var domEle = document.createElement('img');
				jmap.loadedTiles[id] = domEle;
				domEle.setAttribute('src', jmap.tilesDir+id+'.png');
				domEle.setAttribute('class', 'jmap-tile');
				domEle.setAttribute('id', id);
				var pos = tileIdToPos(id);
				domEle.style.left = pos.left;
				domEle.style.top = pos.top;
				domEle.onclick = handleEventBldgUnclick;
				jmap.map.appendChild(domEle);
				setupTileDrag(domEle);
				loadTileBldgs(id);
			}
		}
	}
	//jmap.tiles = $('.jmap-tile');
}

//return bounds on which tiles should be loaded right now, with edge checking
function tilesOnMap() {
	return {
		minX: Math.floor(jmap.dispX/jmap.tileSZ),
		minY: Math.floor(jmap.dispY/jmap.tileSZ),
		maxX: Math.ceil(Math.min(jmap.mapBounds.x2, jmap.dispX+jmap.mapContainer.offsetWidth) / jmap.tileSZ)-1,
		maxY: Math.ceil(Math.min(jmap.mapBounds.y2, jmap.dispY+jmap.mapContainer.offsetHeight) / jmap.tileSZ)-1
	};
}


/***************************************/
/* For bldg loading function of map */
/***************************************/

//load the bldgs.json file that holds all HTML-element data for the buildings
function loadBldgsJSON() {
	$.ajax(jmap.bldgsFile, {
		async: false,
		dataType: 'json',
		success: function(data) {
			jmap.bldgsTile = data.bldgsTile;
			jmap.bldgsInfo = data.bldgsInfo;
		},
		error: handleAjaxError
	});
}

// load and set up hover/click for buildings that are on the loaded tile identified by 'id'
function loadTileBldgs(id) {
	var bldgsOnTile = jmap.bldgsTile[id];
	if (bldgsOnTile == undefined) return;
	for (index in bldgsOnTile) {
		var id = bldgsOnTile[index];
		if (jmap.loadedBldgs[id] == undefined) {
			var bldg = jmap.bldgsInfo[id];
			var domEle = document.createElement('img');
			jmap.loadedBldgs[id] = {'domEle':domEle};
			domEle.setAttribute('class', 'jmap-bldg');
			domEle.setAttribute('id', id);
			domEle.setAttribute('style', 'z-index:'+bldg.zIndex+';');
			setupBldg(domEle);
			domEle.style.height = bldg.height;
			domEle.style.width = bldg.width;
			domEle.style.left = bldg.left;
			domEle.style.top = bldg.top;
			domEle.onmousedown = function(ev){recordMouseDown(ev, jmap.map);};
			domEle.ondragstart = function(ev){ev.preventDefault();};
			jmap.map.appendChild(domEle);
		}
	}
}


function setupBldg(domEle) {
	if (jevent.bldgCodeHasEvent[bldgIdToCode(domEle.id)] || jevent.activeLayer == 5) {
		if (!jmap.loadedBldgs[domEle.id].event)
			setupEventBldg(domEle);
	} else {
		if (jmap.loadedBldgs[domEle.id].event || jmap.loadedBldgs[domEle.id].event == undefined)
			setupPlainBldg(domEle);
	}
}
function setupPlainBldg(domEle) {
	plainBldgMouseout(domEle);
	domEle.onmouseover = function(ev){plainBldgMouseover(domEle);};
	domEle.onmouseout  = function(ev){plainBldgMouseout(domEle);};
	domEle.onclick = handleEventBldgUnclick;
	$(domEle).removeClass('jmap-bldg-active');
	jmap.loadedBldgs[domEle.id].event = false;
}
function setupEventBldg(domEle) {
	if (jevent.activeLayer != 6) {
		eventBldgMouseout(domEle);
		domEle.onmouseover = function(ev){handleEventBldgMouseover(domEle)};
		domEle.onmouseout  = function(ev){handleEventBldgMouseout(domEle)};
	} else {
		plainBldgMouseout(domEle);
		domEle.onmouseover = function(ev){plainBldgMouseover(domEle);};
		domEle.onmouseout  = function(ev){plainBldgMouseout(domEle);};
	}
	domEle.onclick = function(ev){handleEventBldgClick(ev,domEle);};
	$(domEle).addClass('jmap-bldg-active');
	jmap.loadedBldgs[domEle.id].event = true;
}

function handleEventBldgMouseover(domEle) {
	var bldgCode = bldgIdToCode(domEle.id);
	if (jevent.activeBldg != bldgCode) {
		eventBldgMouseover(domEle);
		if (jevent.activeLayer == 0) {
			for (var eventid in jevent.eventsData) {
				if (jevent.eventsData[eventid].bldgCode == bldgCode)
					eventEntryMouseover(eventid);
			}
		} else if (jevent.activeLayer != 5) {
			eventEntryMouseover(bldgCode);
		}
	}
}
function handleEventBldgMouseout(domEle) {
	var bldgCode = bldgIdToCode(domEle.id);
	if (jevent.activeBldg != bldgCode) {
		eventBldgMouseout(domEle);
		if (jevent.activeLayer == 0) {
			for (var eventid in jevent.eventsData) {
				if (jevent.eventsData[eventid].bldgCode == bldgCode)
					eventEntryMouseout(eventid);
			}
		} else if (jevent.activeLayer != 5) {
			eventEntryMouseout(bldgCode);
		}
	}
}
function handleEventBldgClick(ev,domEle) {
	var bldgCode = bldgIdToCode(domEle.id);
	if (jevent.activeBldg != bldgCode) {
		if (jevent.activeBldg != null) {
			if (jevent.activeLayer != 0 && jevent.activeLayer != 5)
				eventEntryMouseout(jevent.activeBldg);
			activeBldgRefresh();
		}
		jevent.activeBldg = bldgCode;
		eventBldgMouseover(domEle);
		if (jevent.activeLayer == 0 || jevent.activeLayer == 5)
			AJAXdataForBldg(bldgCode);
		else {
			var eventEntry = document.getElementById('event-entry-'+bldgCode);
			eventEntryScroll(eventEntry);
		}
	}
}
function handleEventBldgUnclick() {
	if (jevent.activeBldg != null) {
		var oldBldgCode = jevent.activeBldg;
		activeBldgRefresh();
		/* Refresh the info-bot */
		if (jevent.activeLayer == 0)
			AJAXdataForAllBldgs();
		else if (jevent.activeLayer == 5)
			hideInfoEvent();
		else
			eventEntryMouseout(oldBldgCode);
	}
}


/***************************************/
/* Click, Mouseover/out actions for bldgs and events */
/***************************************/

function plainBldgMouseover(domEle) {domEle.src=jmap.bldgsDir+domEle.id+jmap.bldgsHoverSrc;}
function plainBldgMouseout(domEle) {domEle.src=jmap.bldgsDir+domEle.id+jmap.bldgsDefaultSrc;}
function eventBldgMouseover(domEle) {domEle.src=jmap.bldgsDir+domEle.id+jmap.bldgsEventHoverSrc;}
function eventBldgMouseout(domEle) {domEle.src=jmap.bldgsDir+domEle.id+jmap.bldgsEventSrc;}

function activeBldgRefresh() {
	/* Mouse out the building */
	if (jevent.activeBldg != null) {
		var bldgDict = jmap.loadedBldgs[bldgCodeToId(jevent.activeBldg)];
		if (bldgDict != undefined)
			eventBldgMouseout(bldgDict.domEle);
		jevent.activeBldg = null;
	}
}

function eventEntryMouseover(eventId) {
	var eventEntry = document.getElementById('event-entry-'+eventId);
	eventEntry.style.background='#ECECEC';
	if (jevent.activeLayer == 0 && jdisp.jtlShown) {
		var tlMark = document.getElementById('jtl-mark-'+eventId);
		tlMark.setAttribute('class', 'jtl-mark-hover'); 
		tlMark.style.left = parseInt(tlMark.style.left, 10) - 1;
		tlMark.style.zIndex = parseInt(tlMark.style.zIndex, 10) + 1;
	}
}
function eventEntryMouseout(eventId) {
	var eventEntry = document.getElementById('event-entry-'+eventId);
	eventEntry.style.background='transparent';
	if (jevent.activeLayer == 0 && jdisp.jtlShown) {
		var tlMark = document.getElementById('jtl-mark-'+eventId);
		tlMark.setAttribute('class', 'jtl-mark');
		tlMark.style.left = parseInt(tlMark.style.left, 10) + 1;
		tlMark.style.zIndex = parseInt(tlMark.style.zIndex, 10) - 1;
	}
}
function eventEntryScroll(domEle) {
	var infoBot = $('#info-bot');
	var pos = $(domEle).position().top+infoBot.scrollTop()-infoBot.position().top;
	infoBot.animate({ scrollTop: pos }, 300);
}


/***************************************/
/* For lighting up the correct buildings */
/***************************************/

function AJAXbldgsForFilter() {
	showMapLoading();
	$.ajax(jevent.urlFilteredBldgs, {
		data: getFilterParams(),
		dataType: 'json',
		success: displayFilteredBldgs,
		error: function(jqXHR, textStatus, errorThrown) {
			hideMapLoading();
			handleAjaxError(jqXHR, textStatus, errorThrown);
		}
	});
}

/* Grays and un-grays the correct bldgs, given the `data` of bldgs with events */
function displayFilteredBldgs(data) {
	//data.bldgs = true for building codes that should be lit up
	for (var bldgCode in jevent.bldgCodeHasEvent)
		jevent.bldgCodeHasEvent[bldgCode] = false;
	for (var i in data.bldgs)
		jevent.bldgCodeHasEvent[data.bldgs[i]] = true;
	for (var id in jmap.loadedBldgs)
		setupBldg(jmap.loadedBldgs[id].domEle);
	hideMapLoading();
}
/* Grays and un-grays the correct bldgs, given the `bldgCode` of bldg clicked */
function displayLocationBldgs(bldgCode) {
	for (var code in jevent.bldgCodeHasEvent)
		jevent.bldgCodeHasEvent[code] = false;
	jevent.bldgCodeHasEvent[bldgCode] = true;
	for (var id in jmap.loadedBldgs)
		setupBldg(jmap.loadedBldgs[id].domEle);
}


/***************************************/
/* Map interactive functionality */
/***************************************/

function centerOnBldg(bldgCode) {
	var bldgId = bldgCodeToId(bldgCode);
	var bldgObject = jmap.bldgsInfo[bldgId];
	
	// jump to new center coords, refresh tiles
	centroid = mapCenterToDisp(bldgObject.left + bldgObject.width/2, bldgObject.top + bldgObject.height/2);
	jmap.dispX = centroid.x;	
	jmap.dispY = centroid.y;
	$(jmap.map).animate({
		left: -jmap.dispX,
		top: -jmap.dispY,
	}, {
		duration: 200,
		complete: function() {
			loadTiles();
		}
	});
}

function showMapLoading() {
	if (!jmap.mapLoading) {
		var domEle = document.createElement('div');
		domEle.setAttribute('id','map-loading');
		domEle.setAttribute('class','map-box');
		domEle.innerHTML = jevent.htmlLoading;
		jmap.mapContainer.appendChild(domEle);
		jmap.mapLoading = true;
	}
}
function hideMapLoading() {
	if (jmap.mapLoading) {
		jmap.mapContainer.removeChild(document.getElementById('map-loading'));
		jmap.mapLoading = false;
	}
}




/***************************************************************************/
/***************************************************************************/
/***************************************************************************/

/***************************************/
/* For parsing filters into GET params  */
/***************************************/

/* Called when the events/hours/menus/etc tabs are clicked. Changes the filters
 * displayed + loads bldgs for filter + reloads events for filter */
function handleLayerChange(newLayer) {
	if (jevent.activeLayer != newLayer) {
		activeBldgRefresh();
		
		hideInfoEvent();
		var oldLayer = jevent.activeLayer;
		jevent.activeLayer = newLayer;
		
		/* Must clear all buildings if changing from 5 */
		if (oldLayer == 5) {
			for (var id in jmap.loadedBldgs)
				setupPlainBldg(jmap.loadedBldgs[id].domEle);
		}
		/* Must set all buildings if changing to 5 */
		if (jevent.activeLayer == 5) {
			for (var id in jmap.loadedBldgs)
				setupEventBldg(jmap.loadedBldgs[id].domEle);
		}
		else {
			AJAXbldgsForFilter();
			AJAXdataForAllBldgs();
		}
	}
}
/* Called when any specific filters for any particular events/hours/menus/etc tab
 * are clicked. Loads bldgs for filter + reloads events for filter */
function handleFilterChange() {
	AJAXbldgsForFilter();
	if (jevent.activeBldg != null)
		AJAXdataForBldg(jevent.activeBldg);
	else
        AJAXdataForAllBldgs();
}

/* These return the GET params that should be sent in every AJAX call */
function getFilterParams() {
	var get_params = {type: jevent.activeLayer};
	if (jevent.activeLayer == 0) {
		//get dates from JTL if searching events
		var p = getJTLParams();
		var eventParams = {
			m0: p.startDate.getMonth()+1,
			d0: p.startDate.getDate(),
			y0: p.startDate.getFullYear(),
			nDays: p.nDays,
			h0: p.startTime[0]%24,
			i0: p.startTime[1],
			h1: p.endTime[0]%24,
			i1: p.endTime[1],
		}
		$.extend(get_params, eventParams);
	}
	return get_params;
}



/***************************************/
/* For rendering event/etc data in the info box */ 
/***************************************/

function AJAXdataForAllBldgs() {
	showInfoLoading();
	$.ajax(jevent.urlFilteredDataAll, {
		data: getFilterParams(),
		dataType: 'json',
		success: handleDataAJAX,
		error: function(jqXHR, textStatus, errorThrown) {
			hideInfoEvent();
			handleAjaxError(jqXHR, textStatus, errorThrown);
		}
	});
}

function AJAXdataForBldg(bldgCode) {
	showInfoLoading();
	$.ajax(jevent.urlFilteredDataBldg+bldgCode, {
		data: getFilterParams(),
		dataType: 'json',
		success: handleDataAJAX,
		error: function(jqXHR, textStatus, errorThrown) {
			hideInfoEvent();
			handleAjaxError(jqXHR, textStatus, errorThrown);
		}
	});
}

/* Success callback for AJAXdataFor__ */
function handleDataAJAX(data) {
	if (jevent.activeBldg != data.bldgCode) {
		activeBldgRefresh();
		if (data.bldgCode != undefined) {
			jevent.activeBldg = data.bldgCode;
			eventBldgMouseover(jmap.loadedBldgs[bldgCodeToId(data.bldgCode)].domEle);
		}
	}
	$('#info-bot').html(data.html);
	if (jevent.activeLayer == 0) {
		for (var eventid in jevent.eventsData)
			$('#jtl-mark-'+eventid).tipsy('hide');
		jevent.eventsData = data.eventsData;
		jmap.markData = data.markData;
		loadTimeline(jmap.markData);
		showTimelineToggle();
	}
	else if (jevent.activeLayer != 5) {
		$('#info-timestamp-'+jevent.activeLayer).html('Last updated ' + data.timestamp);
		
	}
}

function showInfoLoading() {
	$('#info-bot').html(jevent.htmlLoading);
    $('#info-timestamp-'+jevent.activeLayer).html('');
}

function hideInfoEvent() {
	jevent.activeBldg = null;
	$('#info-bot').html('');
}


