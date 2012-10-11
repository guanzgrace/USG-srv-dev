tigerapps = {

    initializeTigerapps: function() {
        console.log("up and running");
        setInterval(tigerapps.cycleFeaturedApp, 4000);

    },

    featured_app: 0,

    pause_slideshow: false,

    cycleFeaturedApp: function() {
        if (tigerapps.pause_slideshow == false) {
            tigerapps.featured_app = (tigerapps.featured_app + 1) % 5;
            tigerapps.setFeaturedApp(tigerapps.featured_app);
        }
    },
 
    userSelectFeaturedApp: function(feature_number) {
        tigerapps.pause_slideshow = true;
        tigerapps.featured_app = feature_number;
        tigerapps.setFeaturedApp(feature_number);
        setTimeout("tigerapps.pause_slideshow = false", 4000);
    },

    setFeaturedApp: function(feature_number) { 
        $(".app_preview").each(function () {
            $(this).css("background-color", "#707070");
        });
        $("#app_preview_" + feature_number.toString()).css("background-color", "#202020"); 
        $("#photo_row").animate({"left": (feature_number*-600).toString() + "px"}, 1000); 
        
    }
};
