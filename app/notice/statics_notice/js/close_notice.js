// close_notice.js

// тихое удаление уведомлений с помощью ajax

// :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

var j = jQuery.noConflict();

// :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

j(function() {
    j('.close').click(function(event) {
        var target = event.target || window.event.target;
        var parent = target.parentNode.parentNode;
        var notice_id = parent.id.slice(7);
        var piece_url = window.location.href.slice(0, -6);
        
        parent.style.display = 'none';

        j.post(
            `${piece_url}notice/${notice_id}/...del`
        ).done(function(response) {
            if (response['success']) {
                var counter = Number(j('header .Counter').text());
                counter -= 1;
                j('header .Counter').text(counter);
            }
        })
    })
})
