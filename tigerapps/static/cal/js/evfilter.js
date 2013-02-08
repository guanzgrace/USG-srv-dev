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

function evfilterReq() {
    var ts = $('.evfilter-timeselect:checked')[0].id;
    var sd = $.datepicker.formatDate("yymmdd", $('#evfilter-datepicker').datepicker('getDate'));
    console.log(ts);
    console.log(sd);
    $.get('/evlist/gen/ajax/', {ts: ts, sd: sd, },
        evfilterResp, 'json');
}

function evfilterResp(data, textStatus, jqXHR) {
    var td = data.evlist_time_dict;
    console.log(td);
    $('#evfilter-datepicker').rangepicker(td.ts, td.sd, td.ed)
    $('#evlist-title').html(data.evlist_title);
    $('#evlist-subtitle').html(data.evlist_subtitle);
    $('#evlist-inner').html(data.evlist_inner);
    evlistInit();
}
