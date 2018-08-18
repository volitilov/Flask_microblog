// close_flash.js

// Применяется делегированная обработка события нажатия по закрытию
// flash-сообщений.

// :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

var j = jQuery.noConflict();

// :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

j(function() {
    j('.main').on('click', '.closeFlash_btn', function(e) {
        target = e.target || window.e.target;
        target.parentNode.style.display = 'none';
    })
})
