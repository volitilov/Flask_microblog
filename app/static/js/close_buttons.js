// close_buttons.js

//

// :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

var closeFlash_btns = document.querySelectorAll('.closeFlash_btn');
var closeNotice_btns = document.querySelectorAll('.closeNotice_btn');

// :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

for (var i=0; i < closeFlash_btns.length; i++) {
    closeFlash_btns[i].addEventListener('click', function(event) {
        target = event.target || window.event.target;
        target.parentNode.style.display = 'none';
    });
}


for (var i=0; i < closeNotice_btns.length; i++) {
    closeNotice_btns[i].addEventListener('click', function(event) {
        target = event.target || window.event.target;
        target.parentNode.parentNode.style.display = 'none';
    });
}