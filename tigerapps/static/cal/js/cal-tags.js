function clearTag() {
    var tag_element = $('#id_cluster_tags_ui');
    tag_element.val(tag_element.val().replace(/\W/g, ''));
}
function submitTag() {
    $('#id_cluster_tags_ui').textext()[0].tags().addTags([ $.trim($('#id_cluster_tags_ui').val().replace(/\W/g, '')) ]);
    $('#id_cluster_tags_ui').val('');
}
function prepareTags() {
   $('#id_cluster_tags_ui').css('width', '240px');
   $('#id_cluster_tags_ui').textext({
        plugins : 'tags prompt focus autocomplete ajax arrow',
        prompt : 'Choose or add your own...',
        ajax : {
          url : '/ajax/alltags/',
          dataType : 'json',
          cacheResults : true
        }
    });
    $("#id_cluster_tags_ui").keyup(function () {
      if ((event.which == 32 || event.which == 44) && $.trim($('#id_cluster_tags_ui').val().replace(/\W/g, '')) != "") {
        submitTag();
      }
        clearTag();
    });
    $("#id_cluster_tags_ui").focusout( function () {
        setTimeout("submitTag()", 250);
    });
}
