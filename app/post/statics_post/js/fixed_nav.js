// fixed_nav.js

// Фиксирует навигацию по посту при скроле

// :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

var j = jQuery.noConflict();

// :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

var StickyElement = function(node) {
    var doc = j(document), 
        fixed = false,
        anchor = node.find('.nav-post'),
        content = node.find('.menu');

    
    j(window).scroll(function(e) {
        var docTop = doc.scrollTop(),
            anchorTop = anchor.offset().top;
        
        if (docTop > anchorTop) {
            if (!fixed) {
                anchor.height(content.outerHeight());
                content.addClass('fixed');        
                fixed = true;
            }
        }  else   {
            if (fixed) {
                anchor.height(0);
                content.removeClass('fixed'); 
                fixed = false;
            }
        }
    })
};
  
var demo = new StickyElement(j('#sticky'));



// свернуть навигацию по публикациям для удобного чтения
j('.nav-publications .menu').children('.menu-item').each(function(index, item) {
    j(item).toggle(250);
});