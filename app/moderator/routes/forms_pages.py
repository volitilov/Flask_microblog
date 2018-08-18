# moderator/routes/forms_pages.py

# Обрабатывает запросы от форм

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import flash, redirect, url_for, jsonify

from .. import (
    # blueprint
    moderator,

    # forms
    AddNotice_form,

    # utils
    is_moderator, create_response, flash_errors,

    # models
    Post, Notice, UserSettings,

    # database
    db
)


# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@moderator.route('/moderator/posts/<int:id>...return', methods=['POST'])
@is_moderator
def returnPostForm_req(id):
    '''Обрабатывает запросы на отправку уведомлений пользователям о том, 
    что их публикации необходимо доработать.'''
    form = AddNotice_form()
    post = Post.query.get_or_404(id)

    if form.validate():
        user_settings = UserSettings.query.filter_by(state='custom', profile=post.author).first()
        post.state = 'develop'
        
        if user_settings.post_moderated:
            title = 'Moderator'
            body = 'Пост: <a href="{}">{}</a> <br>'.format(
                url_for('post.post_page', id=post.id),
                post.title)
            body = body + form.body.data
            notice = Notice(title=title, body=body, author=post.author)
            db.session.add(notice)

        db.session.add(post)    
        db.session.commit()
        
        flash(category='success', message='Пост успешно отправлен на доработку')
        return jsonify({'next_url': url_for('moderator.posts_page')})

    return jsonify({'errors': flash_errors(form)}) 

