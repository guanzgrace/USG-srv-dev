tigerapps = {

    initializeTigerapps: function() {
        console.log("up and running");
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
                var desc_id = $(this).attr("id").substring(5);
                console.log("SHOWING :" + desc_id);
                $("#" + desc_id).show();
            });
        });

    }
};
