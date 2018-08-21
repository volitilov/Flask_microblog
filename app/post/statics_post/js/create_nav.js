// create_nav.js

// Создаёт навигацию по посту с полученных данных с сервера

// :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

var j = jQuery.noConflict();

// :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

j(function() {
    var elem = j('.nav-post ol');
    elem.hide();
        
    j(elem).children().each(function(index, item) {
        var content = j(item).find('a').text();
        var content_url = j(item).find('a').attr('href');
        var html_elem = `<a class="menu-item" rel="nofollow" href="${content_url}">${content}</a>`;
        
        j('.nav-post .menu').append(html_elem);
    });

})

