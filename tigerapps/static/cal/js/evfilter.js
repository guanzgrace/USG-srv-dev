$.fn.showSpinner = function() {
    this.html('<img src="/static/shared/img/loading-spinner.gif" class="loading-spinner">');
}

function evlistInit() {
    $('.rsvp_indicator').cluetip({
      showTitle: true, // hide the clueTip's heading
      splitTitle: '|',
      width: 540,
      clickThrough: true,
      cluetipClass: 'jtip', 
      arrows: false, 
      dropShadow: true,
      hoverIntent: false,
      sticky: false,
      mouseOutClose: true,
    });
    Shadowbox.init();
}

function evfilterClear() {
    $('#evfilter-tag-current').attr('id', '');
    $('#evfilter-feat-current').attr('id', '');
    $('#evfilter-query').val('');
    evlistReq();
    return false;
}

function evfilterTagOnClick(ev) {
    if (this.id == 'evfilter-tag-current') {
        $(this).attr('id', '');
        evlistReq();
    } else {
        $('#evfilter-tag-current').attr('id', '');
        $(this).attr('id', 'evfilter-tag-current');
        evlistReq();
    }
}

function evfilterFeatOnClick(ev) {
    if (this.id == 'evfilter-feat-current') {
        $(this).attr('id', '');
        evlistReq();
    } else {
        $('#evfilter-feat-current').attr('id', '');
        $(this).attr('id', 'evfilter-feat-current');
        evlistReq();
    }
}


function evlistReq(changedDates) {
    $('#evlist-inner').showSpinner();

    var ts = $('#evfilter-ts input:checked')[0].id;
    var sd = $.datepicker.formatDate("yymmdd", $('#evfilter-datepicker').datepicker('getDate'));
    var data = {ts: ts, sd: sd};

    if (changedDates == undefined) {
        var query = $('#evfilter-query').val();
        if (query) { data.query = query; hasStuff = true; }
        var tag = $('#evfilter-tag-current').attr('rel');
        if (tag) { data.tag = tag; hasStuff = true; }
        var feat = $('#evfilter-feat-current').attr('rel');
        if (feat) { data.feat = feat; hasStuff = true; }
    } else {
        data.changedDates = true;
        $('#evfilter-tags').showSpinner();
        $('#evfilter-feats').showSpinner();
        $('#evfilter-query').val('');
    }

    console.log(data);
    $.ajax({
        url: '/evlist/gen/ajax/',
        beforeSend: function(xhr) {
        },
        data: data,
        success: evlistResp,
        dataType: 'json',
    });
}

function evlistResp(data, textStatus, jqXHR) {
    var td = data.evlist_time_dict;
    console.log(td);
    $('#evfilter-datepicker').rangepicker(td.ts, td.sd, td.ed);
	$('#evlist-title').html(data.evlist_title);
	$('#evlist-dates').html(data.evlist_dates);
    $('#evlist-inner').html(data.evlist_inner);
    evlistInit();

    var fd = data.evlist_filter_dict;
    console.log(fd);
    if (fd.tagsHtml) {
        $('#evfilter-tags').html(fd.tagsHtml);
        $('.evfilter-tag').click(evfilterTagOnClick);
    }
    if (fd.featsHtml) {
        $('#evfilter-feats').html(fd.featsHtml);
        $('.evfilter-feat').click(evfilterFeatOnClick);
    }
}
