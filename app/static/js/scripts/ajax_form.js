// ajax_login.js

// Серверная валидация данных форм с помощью ajax. Работает для всех 
// форм, только для данного ресурса.

// Необходимые условия:
// - в форме должно быть указанно ('method', 'action')
// - сервер должен вернуть ('next_url', в противном случае 'errors' и 
//   'flash' если есть)

// Пример 'errors':
// - {'error': 'текст ошибки', 'field': 'название поля (id поля)'}
// Пример 'flash' если есть:
// - {'category': 'категория ошибки', 'message': 'тест сообщения'}

// :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

var j = jQuery.noConflict();

// :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

j(function() {
    var form = j('form');
    
    form.submit(function(e) {
        var data = new FormData;

        j(this).find('input, textarea').each(function(index, elem) {
            var elem_id = j(elem).attr('id');
            var elem_val = j(elem).val();
            var form_group = j(`#${ elem_id }`).parent().parent();

            form_group.removeClass('errored');
            j('dd.error').remove();
            
            data.append(`${ elem_id }`, elem_val)
            
            if (j(elem).attr('type') == 'file') {
                data.append(`${ elem_id }`, j(elem).prop('files')[0]);
            }

        });
        
        j.ajax({
            url: form.attr('action'),
            type: form.attr('method'),
            contentType: false,
            processData: false,
            data: data
        }).done(function(data) {
            if (data['next_url']) {
                window.location.replace(data['next_url']);
            } else {
                var errors = data['errors'];
                var flash = data['flash'];

                if (errors) {
                    for (error in errors) {
                        var field = errors[error]['field'];
                        var error =  errors[error]['error'];
                        var form_group = j('#'+field).parent().parent();
                        
                        form_group.addClass('errored');
                        form_group.append(`<dd class="error">${ error }</dd>`);
                    }
                }

                if (flash) {
                    var category = flash['category'];
                    var message = flash['message'];

                    var message_html = `
                        <li class="flash flash-${ category }">
                            ${ message }
                            <button class="close closeFlash_btn">&times;</button>
                        </li>`

                    j('.main').prepend(`<ul class="flash-messages">${ message_html }</ul>`);
                }
            }
        }).fail(function(data) {
            console.log(data);
        });

        e.preventDefault();
    })
})