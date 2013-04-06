/***************************************/
/* General display setup */
/***************************************/

jdisp = {};
function displayInit() {
	mapInit();
	
	jdisp.jtl = $("#jtl-content")
	jdisp.jtlContainer = $("#jmap-jtl");
	jdisp.jtlToggle = $("#jtl-toggle");
	jdisp.jtlToggleArrow = jdisp.jtlToggle.children("span");
	
	$("input:submit").button();
	$(":button").button();
	$("#layer-tabs").buttonset();
	
	//timeline display
	$("#jtl-startDate").datepicker({
        firstDay: 1,
	});
	$("#jtl-startDate").datepicker('setDate', new Date());
	setupJTLSlider();
	setupJTLDisplay();

	window.onresize = loadWindowSizeDependent;
	setupLayers();
	setupLayerFilters();
    loadWindowSizeDependent();

    $("#jmap-about a").tipsy({gravity:'sw',html:true,manual:true});
}

function loadWindowSizeDependent() {
	var newHeight = jmap.info.offsetHeight-jmap.infoTop.offsetHeight-20;
	$('#info-bot').css('height', newHeight+'px');
	loadTiles();
	if (jevent.activeLayer == 0) {
		loadTimeline(jmap.markData);
	}
    var tbar = $('#jmap-topbar'),
        logo = $('#logo'),
        ele1 = $('#layer-tabs'),
        h = tbar.height();
    $('#jmap-container').css('top', h+1+'px');
    if (h < 60) {
        logo.css('margin-bottom','12px');
        ele1.css('margin-bottom','12px');
    }
    else if (h < 120) {
        logo.css('margin-bottom','0px');
        ele1.css('margin-bottom','12px');
    } else {
        logo.css('margin-bottom','0px');
        ele1.css('margin-bottom','0px');
    }
}


/***************************************/
/* Tabs display */ 
/***************************************/

/* These setup the layer tabs so that AJAX calls are sent
 * when the layer is changed */
function setupLayers() {
	$("#layer-tabs input").change(function(ev) {
		displayLayer(ev.target.value);
		handleLayerChange(ev.target.value);
		loadWindowSizeDependent();
	});
	displayLayer(0);
	jdisp.jtlShown = true;
	handleLayerChange(0);
}
function displayLayer(layer) {
	$(".top-tab").css('display', 'none');
	$("#top-tab-"+layer).css('display', 'block');
    if (layer == 0) showTimelineToggle();
    else            hideTimelineToggle();
}

/* These setup the layer-specific filters so that AJAX calls
 * are sent when the filters are changed */
function setupLayerFilters() {
	$('.jtl-params').change(function() {
		handleFilterChange();
	});
	setupLocationSearch();
}

/* load the JSON file that holds all HTML-element data
 * for the buildings */
function setupLocationSearch() {
    var input = $("#location-search"),
        submit = $('#location-search-submit'),
        form = $("#location-search-form");

    input.focus(function(event) {
        $('#filter-locations').click();
    });

	/* setup location search autocomplete */
	$.ajax('/widget/locations/setup/', {		
		dataType: 'json',
		success: function(data) {
			jevent.bldgNames = data;
			var bldgNameList = [];
			var i = 0;
			for (name in data)
				bldgNameList[i++] = name;
			input.autocomplete({
                autoFocus: true,
				delay: 0,
				minLength: 2,
				source: bldgNameList,
                select: function(event, ui) {
                    input.val(ui.item.value);
                    form.submit();
                },
			})/*.data("ui-autocomplete")._renderItem = function(ul, item) {
                var re = new RegExp(input.val(), 'gi');
                return $('<li>')
                    .append('<a>' + item.label.replace(re, '<b>$&</b>') + '</a>')
                    .appendTo(ul);
            }*/;
		},
		error: handleAjaxError
	});
	
	/* setup location search submit */
	form.submit(function(event) {
		event.preventDefault();
        $('#filter-locations').click()

		// get submitted building's code, center map on it, and display its events
		var bldgName = $('#location-search').val();
		var bldgCode = jevent.bldgNames[bldgName];
		if (bldgCode != undefined) {
			displayLocationBldgs(bldgCode);
			centerOnBldg(bldgCode);
			AJAXdataForBldg(bldgCode);
		} else {
			submit.effect('shake',{times:5,distance:3},30);
			input.val('');
		}
	});
}

/***************************************/
/* Tab-specific filters display */ 
/***************************************/

function setupJTLSlider() {
    oldLeft = -1;
    oldRight = -1;
    var sliderEle = $("#jtl-slider");
	
    sliderEle.slider({
        range: true,
        min: 0,
        max: 48,
        values: [16, 48], //initial
        slide: function( event, ui ) {
        	//sliderLeftTimeVal and sliderRightTimeVal will contain arrays where the zeroth 
        	//element is the hour (0-23) and the first element is the minutes (0 or 30)
        	if (ui.values[1] - ui.values[0] < 4) return false;
        	var startTime = indexToTimeArr(ui.values[0]);
    		var endTime = indexToTimeArr(ui.values[1]);
            $("#jtl-slider-start").val(printTime(startTime));
            $("#jtl-slider-end").val(printTime(endTime));
        },
        
        stop: function (event, ui) {
        	if (oldLeft != ui.values[0] || oldRight != ui.values[1]) {
            	var startTime = indexToTimeArr(ui.values[0]);
        		var endTime = indexToTimeArr(ui.values[1]);
                $("#jtl-startTime").val(printTimeMilit(startTime));
                $("#jtl-endTime").val(printTimeMilit(endTime));
            	oldLeft = ui.values[0];
            	oldRight = ui.values[1];
            	
        		handleFilterChange();
            }
        }
    });

	var startTime = indexToTimeArr(sliderEle.slider( "values", 0 ));
	var endTime = indexToTimeArr(sliderEle.slider( "values", 1 ));
    $("#jtl-slider-start").val(printTime(startTime));
    $("#jtl-slider-end").val(printTime(endTime));
    $("#jtl-startTime").val(printTimeMilit(startTime));
    $("#jtl-endTime").val(printTimeMilit(endTime));
}

function indexToTimeArr(sliderVal) {
	return [Math.floor(sliderVal/2), (sliderVal%2)*30];
}
function printTimeMilit(timeArr) {
	return timeArr[0] + ':' + timeArr[1];
}
function printTime(timeArr) {
    var hours = timeArr[0];
    hours %= 24
    var am = true;
    if (hours > 12) {
       am = false;
       hours -= 12;
    } else if (hours == 12) {
       am = false;
    } else if (hours == 0) {
       hours = 12;
    }
    zeroPad = ''
    if (timeArr[1] == 0)
    	zeroPad += "0"
    return hours + ":" + timeArr[1] + zeroPad + ' ' + (am ? "AM" : "PM");
}

/* Return dictionary of params in the input box for javascript */
function getJTLParams() {
	//var startDate = $('#jtl-startDate').datepicker("getDate");
	var inDate = $('#jtl-startDate').val().split('/');
	var startDate = new Date();
	clearDateTime(startDate);
	startDate.setFullYear(inDate[2]);
	startDate.setMonth(inDate[0]-1);
	startDate.setDate(inDate[1]);
	var nDays = $('#jtl-nDays').val();
	var startTime = $('#jtl-startTime').val().split(':');
	var endTime = $('#jtl-endTime').val().split(':');
	return {startDate:startDate, nDays:nDays, startTime:startTime, endTime:endTime};
}


/***************************************/
/* Timeline display */ 
/***************************************/

function setupJTLDisplay() {
	jdisp.jtlShown = false;
	jdisp.jtlToggle.click(function() {
		if (jdisp.jtlShown)
			hideTimeline();
		else
			showTimeline();
	});
}
function showTimelineToggle() {
	jdisp.jtlToggle.show();
	if (jdisp.jtlShown)
        showTimeline();
    else
        hideTimeline();
}
function hideTimelineToggle() {
	jdisp.jtlToggle.hide();
    if (jdisp.jtlShown) {
        hideTimeline();
        jdisp.jtlShown = true;
    }
}
function showTimeline() {
	jdisp.jtlContainer.animate({
		right:'380px'
	}, 100);
	jdisp.jtlToggle.animate({
		right:'542px'
	}, 100);
	jdisp.jtlToggleArrow.attr('class', 'ui-icon ui-icon-carat-1-e');
	$('#jmap-info').addClass('jmap-info-expanded');
	jdisp.jtlShown = true;
}
function hideTimeline() {
	jdisp.jtlContainer.animate({
		right:'218px'
	}, 100);
	jdisp.jtlToggle.animate({
		right:'380px'
	}, 100);
    jdisp.jtlToggleArrow.attr('class', 'ui-icon ui-icon-carat-1-w');
	$('#jmap-info').removeClass('jmap-info-expanded');
	jdisp.jtlShown = false;
}


function loadTimeline(markData) {
	$(jdisp.jtl).timeline(getJTLParams(), markData,
			handleEventEntryMouseover,
			handleEventEntryMouseout,
			handleEventTickClick);
	for (var eventid in jevent.eventsData) {
		var $domEle = $('#jtl-mark-'+eventid);
		$domEle.attr('title',jevent.eventsData[eventid].tooltip);
		$domEle.tipsy({gravity:'e',html:true,manual:true});
	}
}

function handleEventEntryMouseover(eventId) {
	eventEntryMouseover(eventId);
	if (jevent.activeLayer == 0 && jdisp.jtlShown) {
		$('#jtl-mark-'+eventId).tipsy('show');
	}
	var bldgCode;
	if (jevent.activeLayer == 0)
		bldgCode = jevent.eventsData[eventId].bldgCode;
	else
		bldgCode = eventId;
	var bldgDict = jmap.loadedBldgs[bldgCodeToId(bldgCode)];
	if (bldgDict != undefined) eventBldgMouseover(bldgDict.domEle);
}
function handleEventEntryMouseout(eventId) {
	eventEntryMouseout(eventId);
	if (jevent.activeLayer == 0 && jdisp.jtlShown) {
		$('#jtl-mark-'+eventId).tipsy('hide');
	}
	if (jevent.activeLayer == 0)
		bldgCode = jevent.eventsData[eventId].bldgCode;
	else
		bldgCode = eventId;
	var bldgDict = jmap.loadedBldgs[bldgCodeToId(bldgCode)];
	if (bldgDict != undefined) eventBldgMouseout(bldgDict.domEle);
}
function handleEventEntryClick(eventId) {
	var eventEntry = document.getElementById('event-entry-'+eventId);
	if (jevent.activeLayer == 0) {
		$(eventEntry).find('.info-event-dots').toggle();
		$(eventEntry).find('.info-event-long').toggle(300);
	}
}
function handleEventTickClick(eventId) {
	var eventEntry = document.getElementById('event-entry-'+eventId);
    eventEntryScroll(eventEntry);
    $(eventEntry).find('.info-event-dots').hide();
    $(eventEntry).find('.info-event-long').show(300);
}


/***************************************/
/* Utility functions */
/***************************************/

function clearDateTime(d) {
	d.setHours(0);d.setMinutes(0);d.setSeconds(0);d.setMilliseconds(0);
}

function handleAjaxError(jqXHR, textStatus, errorThrown) {
	var e1 = 'Sorry! A server error occurred while you were browsing the page: "'+errorThrown+'".';
	var e2 = 'Please contact our team at it@princetonusg.com if you see this message again.';
    if (confirm(e1+'\n\n'+e2+'\n\nView error?')) {
        win = window.open();
        win.document.write(jqXHR.responseText);
    }
	$('#info-bot').html('<div class="info-error">'+e1+'<br/><br/>'+e2+'</div>');
}

