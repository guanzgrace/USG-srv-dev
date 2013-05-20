var setSectionOptions = function(sections){
// 	var height = $("#container").height();
// 	$("#container").height(height);
	$("#submit").show();
	$("#have-label").show();
	$("#have-options").empty();
	_.each(sections, function(section){
		var el = $('<label class="radio"><input name="have" class="have-option" value="' + section.number + '" type="radio">' + section.name + '</label>');
		$("#have-options").append(el);
	});
	$("#want-label").show();
	$("#want-options").empty();
	_.each(sections, function(section){
		var el = $('<label class="checkbox"><input name="want" class="want-option" ' + ' value="' + section.number + '" type="checkbox">' + section.name + '</label>');
		$("#want-options").append(el);
	});

	// Disable the corresponding checkbox in the "have" column.
	$(".have-option").click(function(eventData){
		var haveOptionEl = $(eventData.target);
		var sectionNumber = haveOptionEl.val();
		$('.want-option').attr('checked', false);
		$('.want-option').attr('disabled', false);
		$('.want-option[value="' + sectionNumber + '"]').attr('disabled', true);
	});
	
	$("body").attr("background", "-webkit-linear-gradient(#FFFFFF, #EEEEEE)");
	var width = $("#want-options").width();
	$("#options-div").width(60 + width * 2);
	
// 	$('#container').css('height', 'auto');
// 	var autoHeight = $('#container').height();
// 	$('#container').height(height).animate({height: autoHeight}, 300);
}

var submit = function(querystring){
	var url = "swaprequest" + querystring;	
	window.location.href = url;			
}

function get_user_query() {
    name = 'netid';
    name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
    var regexS = "[\\?&]" + name + "=([^&#]*)";
    var regex = new RegExp(regexS);
    var results = regex.exec(window.location.search);
    if(results == null)
	return "";
    else
	return decodeURIComponent(results[1].replace(/\+/g, " "));
}

var validate = function(){
	var isHasChecked = $(".have-option:checked").length > 0;
	var isWantChecked = $(".want-option:checked").length > 0;

	if (!isHasChecked){
		alert("Please select the section you have.");
		return;
	}

	if (!isWantChecked){
		alert("Please select the section(s) you want.");
		return;
	}

	return true;
}

var mustOverwrite = function(querystring){
	$.get("mustOverwrite" + querystring, function(result){
		return result;
	});
}

// Executed on document load 
$(document).ready(function(){
    
    $('#container').fadeIn();
    
    $.getJSON("courses", function(courses){
	    _.each(courses, function(course){
		    var el = $('<option value="' + course['number'] + '"></option>').text(course['code'])[0];
		    $("#section-select").append(el);
		});
	    
	    $("#section-select").change(function(){
		    var selectedNumber = $("#section-select").val();
		    var selectedCourse = _.find(courses, function(course){return selectedNumber == course.number;});
		    setSectionOptions(selectedCourse.sections);
		});
	});
    
    
    $("#submit").click(function(){
    	if (!validate()) return;
		var courseNumber = $("#section-select").val();	
		var haveNumber = $(".have-option:checked").val();
		var wantNumber = _.map($(".want-option:checked"), function(w){return $(w).val()});
		var user = get_user_query();
		user = user == "" ? 'jmcohen' : user;
		var querystring = "?course=" + courseNumber + "&have=" + haveNumber + "&want=" + wantNumber + "&user=" + user;

		$.get("mustOverwrite" + querystring, function(result){
			if (result == "true"){
				bootbox.confirm("You already have pending swaps for this course. Do you want to overwite them?", function(confirmed){
					if (confirmed){
						submit(querystring);
					}
				});
			} else {
				submit(querystring);
			}
		});

    });
    
    $("#section-select").select2();
});
