# moderator/routes/forms_pages.py

# Обрабатывает страницы с формами

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import flash, redirect, url_for 

from .. import (
    # blueprint
    moderator,

    # forms
    AddNotice_form,

    # utils
    is_moderator, create_response,

    # models
    Post, Notice, UserSettings,

    # data
    page_titles, get_data,

    # database
    db
)


# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@moderator.route('/moderator/posts/<int:id>...return', methods=['GET', 'POST'])
@is_moderator
def returnPost_page(id):
    '''Обрабатывает запросы на отправку уведомлений пользователям о том, 
    что их публикации необходимо доработать.'''
    data = get_data()
    form = AddNotice_form()
    post = Post.query.get_or_404(id)

    if form.validate_on_submit():
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
        return redirect(url_for('moderator.posts_page'))

    return create_response(template='mod_noticePost_form.html', data={
        'title_page': page_titles['returnPost_page'],
        'form': form,
        'post': post,
        'comments': data['comments'],
        'posts': data['posts']
    })