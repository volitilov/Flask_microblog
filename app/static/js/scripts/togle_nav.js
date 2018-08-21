// togle_nav.js

//

// :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

var j = jQuery.noConflict();

// :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

j(function() {
    j('.menu-heading').click(function() {
        var parent = this.parentNode;
        
        j(parent).children('.menu-item').each(function(index, item) {
            j(item).toggle(250);
        });

    })
})
