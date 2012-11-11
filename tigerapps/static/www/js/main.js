tigerapps = {

    initializeTigerapps: function() {
        console.log("up and running");
        tigerapps.setAppSelection();
    },
    
    setAppSelection : function() {
        var desc_apps = $(".desc-app");
        desc_apps.each(function (){
            $(this).click(function () {
                desc_apps.each(function () {
                   $(this).hide();
                });
                $(this).show();
            });
        });

    }
};
