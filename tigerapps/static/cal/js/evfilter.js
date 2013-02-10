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

function timeselectChangeInit() {
    $('.evfilter-tag').click(evfilterTagOnClick);
}

function evfilterClear() {
    $('#evfilter-query').val('');
    $('#evfilter-tag-current').attr('id', '');
    $('#evfilter-feat-current').attr('id', '');
    evfilterReq();
    return false;
}

function evfilterTagOnClick(ev) {
    if (this.id == 'evfilter-tag-current') {
        $(this).attr('id', '');
        evfilterReq();
    } else {
        $('#evfilter-tag-current').attr('id', '');
        $(this).attr('id', 'evfilter-tag-current');
        evfilterReq();
    }
}

function evfilterFeatOnClick(ev) {
    if (this.id == 'evfilter-feat-current') {
        $(this).attr('id', '');
        evfilterReq();
    } else {
        $('#evfilter-feat-current').attr('id', '');
        $(this).attr('id', 'evfilter-feat-current');
        evfilterReq();
    }
}

function evfilterReq() {
    if (rangepicker.onlyAnUpdate) return;

    var ts = $('#evfilter-ts input:checked')[0].id;
    var sd = $.datepicker.formatDate("yymmdd", $('#evfilter-datepicker').datepicker('getDate'));
    var data = {ts: ts, sd: sd};

    var hasStuff = false;
    var query = $('#evfilter-query').val();
    if (query) { data.query = query; hasStuff = true; }
    var tag = $('#evfilter-tag-current').attr('rel');
    if (tag) { data.tag = tag; hasStuff = true; }
    var feat = $('#evfilter-feat-current').attr('rel');
    if (feat) { data.feat = feat; hasStuff = true; }

    if (hasStuff) $('.evfilter-clear').show();
    else $('.evfilter-clear').hide();

    console.log(data);

    $.ajax({
        url: '/evlist/gen/ajax/',
        beforeSend: function(xhr) {
            $('#evlist-loading').show();
            $('#evlist-inner').html('');
        },
        data: data,
        success: evfilterResp,
        dataType: 'json',
    });
}

function evfilterResp(data, textStatus, jqXHR) {
    var td = data.evlist_time_dict;
    console.log(td);
    $('#evfilter-datepicker').rangepicker(td.ts, td.sd, td.ed, td.dp);
	$('#evlist-title').html(data.evlist_title);
	$('#evlist-dates').html(data.evlist_dates);
    $('#evlist-inner').html(data.evlist_inner);
    evlistInit();
    $('#evlist-loading').hide();
}
