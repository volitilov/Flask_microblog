# comment/routes/forms_pages.py

# Обрабатывает запросы от форм

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import redirect, request, url_for, flash, jsonify, abort
from flask_login import current_user, login_required

from .. import (
    # blueprint
    comment,

    # utils
    flash_errors,

    # forms
    AddComment_form,
    
    # models 
    Post, User, Comment, UserSettings, Notice,

    # database
    db
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@comment.route(rule='/comments/...post-<int:id>', methods=['POST'])
@login_required
def addCommentForm_req(id):
    '''Генерирует страницу для добавления комментария'''
    form = AddComment_form()
    post = Post.query.get_or_404(id)

    if form.validate():
        body = form.body.data
        comment = Comment(body=body, post=post, author=current_user)
        comment.state = 'moderation'
        user_settings = UserSettings.query.filter_by(state='custom', profile=comment.post.author).first()

        if user_settings.comments_me:
            notice_title = 'Оставили комментарий к посту'
            notice_body = '''<b>{}</b> - оставил вам комметарий к посту - 
                <b>{}</b><br><br>На данный момент он отправлен к вам на модерацию, 
                <a href="{}">посмотреть</a>'''.format(
                    comment.author.name, comment.post.title, 
                    url_for('user.adminComment_page', username=current_user.name, id=comment.id)
            )
            notice = Notice(title=notice_title, body=notice_body, author=comment.post.author)
            db.session.add(notice)
        
        db.session.add(comment)
        db.session.commit()
        flash(message='Ваш комментарий отправлен на модерацию.')
        return jsonify({'next_url': url_for('post.post_page', id=id)})

    return jsonify({'errors': flash_errors(form)})

    



@comment.route(rule='/comments/<int:comment_id>...edit', methods=['POST'])
@login_required
def editCommentForm_req(comment_id):
    '''Генерирует страницу редактирования комментария'''
    comment = Comment.query.get_or_404(comment_id)
    form = AddComment_form()

    if current_user == comment.author:	
        if form.validate():
            comment.body = form.body.data
            comment.state = 'moderation'

            db.session.add(comment)
            db.session.commit()
            flash(message='Ваш комментарий отправлен на модерацию')
            return jsonify({'next_url': url_for('comment.comment_page', id=comment_id)})
        else:
            return jsonify({'errors': flash_errors(form)})
	
    abort(403)

    