tigerapps = {
    initializeTigerapps: function() {
        tigerapps.setAppSelection();
    },
    
    setAppSelection : function() {
        var desc_apps = $(".desc-app");
        var tile_apps = $(".tile-app");
        tile_apps.each(function (){
            $(this).click(function () {
                desc_apps.each(function () {
                    $(this).hide();
                });
                var desc_id = "desc-" + $(this).attr("id").substring(5);
                $("#" + desc_id).fadeIn();
            });
        });
    }
};
