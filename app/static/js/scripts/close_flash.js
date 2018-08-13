// close_flash.js

//

// :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

var closeFlash_btns = document.querySelectorAll('.closeFlash_btn');

// :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

for (var i=0; i < closeFlash_btns.length; i++) {
    closeFlash_btns[i].addEventListener('click', function(event) {
        target = event.target || window.event.target;
        target.parentNode.style.display = 'none';
    });
}
