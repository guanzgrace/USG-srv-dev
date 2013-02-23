var sug = {

    sugInit: function() {
        $("#new_suggestion_form").submit(function () {
            $.ajax({
                data: $(this).serialize(),
                type: $(this).attr("method"),
                url:  $(this).attr("action"),
                success: function(response) {
                  // filter works here, find works below, idk why
                  $("#suggestion_form_container").replaceWith($(response).filter("#suggestion_form_container"));
                  $("#cast_vote_container").replaceWith($(response).filter("#cast_vote_container"));
                }
            });
           return false;
        });

        $("form.vote_form").submit(function () {
          var id = "#" + $(this).attr("id") + "_container";
          $.ajax({
                data: $(this).serialize(),
                type: $(this).attr("method"),
                url:  $(this).attr("action"),
                success:
                  function(response) {
                    // Update form
                    $(id).replaceWith($(response).find(id));
                    // also update vote count for user
                  }   
            });
           return false;
 
       });
 
    },

    showAddEvent: function () {
      $("#suggestion_form_container").show();
      $("#new_suggestion_button").hide();
    },

    hideAddEvent: function () {
      $("#suggestion_form_container").hide();
      $("#new_suggestion_button").show();
    }

};
