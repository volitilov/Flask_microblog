# moderator/req.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import redirect, request, url_for, flash, current_app

from flask_login import current_user, login_required

from . import moderator
from .utils import is_moderator
from .forms import AddNotice_form
from ..models.post import Post
from ..models.user_settings import UserSettings
from ..models.comment import Comment
from ..models.notice import Notice
from ..models.tag import Tag, Rel_tag
from ..models.post_rating import Post_rating
from ..models.user_settings import UserSettings
from .. import db

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@moderator.route('/posts/<int:id>...confirm')
@is_moderator
def confirmPost_request(id):
    post = Post.query.get_or_404(id)
    post.state = 'public'

    notice_title = 'Модерация публикаций'
    notice_body = 'Пост: <b>{}</b> <br> успешно прошёл модерацию.'.format(post.title)
    notice = Notice(title=notice_title, body=notice_body, author=post.author)
    
    db.session.add_all([post, notice])
    db.session.commit()

    flash(category='success', message='Пост успешно подтверждён')

    return redirect(url_for('moderator.posts_page'))


@moderator.route('/posts/<int:id>...del')
@is_moderator
def deletePost_request(id):
	post = Post.query.get_or_404(id)

	title = 'Модерация публикаций'
	body = '''Пост: <b>{}</b> <br> не прошёл модерацию и был удалён'''.format(post.title)
	notice = Notice(title=title, body=body, author=post.author)

	db.session.add(notice)
	db.session.delete(post)
	db.session.commit()

	flash(category='success', message='Пост успешно удалён')
	return redirect(url_for('moderator.posts_page'))


@moderator.route('/posts/<int:id>...send_notice', methods=['POST'])
@is_moderator
def sendNoticePost_request(id):
    post = Post.query.get_or_404(id)
    form = AddNotice_form()

    if form.validate_on_submit():
        user_settings = UserSettings.query.filter_by(state='custom', profile=post.author).first()
        post.state = 'develop'
        
        if user_settings.post_moderated:
            title = 'Модерация публикаций'
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
    
    else:
        flash(category='error', message='Неправильно заполнена форма')
        return redirect(url_for('moderator.returnPost_page', id=post.id))

