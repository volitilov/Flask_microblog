// scroll_up.js

// Реализует функционал кнопки возврата на верх страницы

// :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

var j = jQuery.noConflict();

// :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

window.onscroll = function() {scrollFunction()};

function scrollFunction() {
    if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
        j("#scrollUp").show();
        j('#scrollUp i').show();
    } else {
        j("#scrollUp").hide();
        j('#scrollUp i').hide();
    }
}


j(function() {
	j('#scrollUp').click(function(event) {
		event = event || window.event;
        event.preventDefault();

        j('html, body').animate({scrollTop : 0}, 800);

        return false;
	})
})