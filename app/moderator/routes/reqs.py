# moderator/routes/reqs.py

# Обрабатывает POST-запросы 
# Работа с данными: добавление, редактирование, удаление

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import redirect, url_for, flash
from flask_login import current_user

from .. import (
    # blueprint
    moderator, 
    
    # utils
    is_moderator,

    # forms
    AddNotice_form,

    # models
    Post, Notice, Tag, Rel_tag, Post_rating,

    # database
    db
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@moderator.route('/moderator/posts/<int:id>...confirm')
@is_moderator
def confirmPost_request(id):
    '''Обрабатывает запросы на успешную модерацию публикаций'''
    post = Post.query.get_or_404(id)
    post.state = 'public'

    notice_title = 'Модерация публикаций'
    notice_body = 'Пост: <a href="{}">{}</a> <br> успешно прошёл модерацию.'.format(
        url_for('post.post_page', id=post.id), post.title)
    notice = Notice(title=notice_title, body=notice_body, author=post.author)
    
    db.session.add_all([post, notice])
    db.session.commit()

    flash(category='success', message='Пост успешно подтверждён')

    return redirect(url_for('moderator.posts_page'))



@moderator.route('/moderator/posts/<int:id>...del')
@is_moderator
def deletePost_request(id):
    '''Обрабатывает запросы на удаление публикаций не прошедших
    модерацию.'''
    post = Post.query.get_or_404(id)

    title = 'Модерация публикаций'
    body = '''Пост: <b>{}</b> <br> не прошёл модерацию и был удалён'''.format(post.title)
    notice = Notice(title=title, body=body, author=post.author)

    post_r = Post_rating.query.filter_by(post=post).all()
    for pr in post_r:
        db.session.delete(pr)

    rel_tags = Rel_tag.query.filter_by(post=post).all()
    for r_t in rel_tags:
        tag = r_t.tag
        tags = Tag.query.filter_by(name=tag.name).all()
        for t in tags:
            if t.posts.count() <= 1:
                db.session.delete(t)
        
        db.session.delete(r_t)

    db.session.add(notice)
    db.session.delete(post)
    db.session.commit()

    flash(category='success', message='Пост успешно удалён')
    return redirect(url_for('moderator.posts_page'))

