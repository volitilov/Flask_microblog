# user/req.py

#

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import redirect, url_for, flash, current_app
from flask_login import current_user, login_required

from . import user
from .forms import EditNotice_form, AddNotice_form
from ..models.notice import Notice
from ..models.comment import Comment
from ..models.user import User
from ..models.user_settings import UserSettings
from ..models.role import Role
from .. import db

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@user.route('/notice/...change_settings', methods=['POST'])
@login_required
def editNotice_request():
    form = EditNotice_form()
    user_settings = UserSettings.query.filter_by(state='custom', profile=current_user).first()

    user_settings.comments_me = form.comments_me.data
    user_settings.follow_me = form.follow_me.data
    user_settings.unfollow_me = form.unfollow_me.data
    user_settings.unsubscribe_me = form.unsubscribe_me.data
    user_settings.comment_moderated = form.comment_moderated.data
    user_settings.post_moderated = form.post_moderated.data

    db.session.add(user_settings)
    db.session.commit()

    flash(category='success', message='Ваши настройки успешно сохранены.')
    return redirect(url_for('user.editNotice_page', username=current_user.name))



@user.route('/notice/...returnDefault_settings')
@login_required
def returnDefaultNoticeSettings_request():
    form = EditNotice_form()
    default = UserSettings.query.filter_by(state='default', profile=current_user).first()
    custom = UserSettings.query.filter_by(state='custom', profile=current_user).first()

    custom.comments_me = default.comments_me
    custom.follow_me = default.follow_me
    custom.unfollow_me = default.unfollow_me
    custom.unsubscribe_me = default.unsubscribe_me
    custom.comment_moderated = default.comment_moderated
    custom.post_moderated = default.post_moderated

    db.session.add(custom)
    db.session.commit()

    flash(category='success', message='Настройки успешно востановлены.')
    return redirect(url_for('user.editNotice_page', username=current_user.name))



@user.route('/admin/comments/<int:id>...confirm')
@login_required
def adminConfirmComment_request(id):
    comment = Comment.query.get_or_404(id)
    comment.state = 'public'

    user_settings = UserSettings.query.filter_by(state='custom', profile=comment.author).first()
    if user_settings.comment_moderated:
        notice_title = 'Модерация комментариев'
        notice_body = '''Ваш <a href="{}">комментарий</a> к посту <a href="{}">{}</a> 
            успешно прошёл модерацию.'''.format(
                url_for('comment.comment_page', username=current_user.name, id=comment.id),
                url_for('post.post_page', id=comment.post.id),
                comment.post.title
        )
        notice = Notice(title=notice_title, body=notice_body, author=comment.author)
        db.session.add(notice)
    
    db.session.add(comment)
    db.session.commit()

    flash(category='success', message='Комментарий успешно подтверждён')

    return redirect(url_for('user.adminComments_page', username=current_user.name))



@user.route('/admin/comments/<int:id>...del')
@login_required
def adminDeleteComment_request(id):
    comment = Comment.query.get_or_404(id)

    db.session.delete(comment)
    db.session.commit()

    return redirect(url_for('user.adminComments_page', username=current_user.name))



@user.route('/admin/comments/<int:id>...send_notice', methods=['POST'])
@login_required
def sendNoticeComment_request(id):
    comment = Comment.query.get_or_404(id)
    form = AddNotice_form()

    if form.validate_on_submit():
        user_settings = UserSettings.query.filter_by(state='custom', profile=comment.author).first()
        comment.state = 'develop'
        
        if user_settings.comment_moderated:
            title = 'Модерация комментариев'
            body = 'Ваш <a href="{}">комментарий</a> <br>'.format(
                url_for('comment.comment_page', username=current_user.name, id=comment.id))
            body = body + form.body.data
            notice = Notice(title=title, body=body, author=comment.author)
            db.session.add(notice)

        db.session.add(comment)    
        db.session.commit()
        
        flash(category='success', message='Комментарий успешно отправлен на доработку')
        return redirect(url_for('user.adminComments_page', username=current_user.name))
    
    else:
        flash(category='error', message='Неправильно заполнена форма')
        return redirect(url_for('user.adminReturnComment_page', id=comment.id))