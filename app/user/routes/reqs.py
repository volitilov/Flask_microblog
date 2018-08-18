# user/routes/reqs.py

# Обрабатывает POST-запросы 
# Работа с данными: добавление, редактирование, удаление

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import redirect, url_for, flash, request, abort
from flask_login import current_user, login_required, fresh_login_required

from .. import (
    # blueprint
    user,

    # forms
    EditNotice_form, AddNotice_form,

    # models
    Notice, Comment, UserSettings, User,

    # database
    db
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::  

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



@user.route('/<username>/admin/comments/<int:id>...confirm')
@login_required
def adminConfirmComment_request(username, id):
    comment = Comment.query.get_or_404(id)
    comment.state = 'public'

    if username != current_user.name:
       abort(403)

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



@user.route('/<username>/admin/comments/<int:id>...del')
@login_required
def adminDeleteComment_request(username, id):
    comment = Comment.query.get_or_404(id)

    if username != current_user.name:
        abort(403)

    db.session.delete(comment)
    db.session.commit()

    return redirect(url_for('user.adminComments_page', username=current_user.name))



@user.route(rule='/delete_account', methods=['POST'])
@fresh_login_required
def deleteAccount_request():
    user = User.query.get(current_user.id)
    for post in user.posts:
        db.session.delete(post)
    for comment in user.comments:
        db.session.delete(comment)
        
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('main.home_page'))



@user.route(rule='/change_email/<token>')
@login_required
def changeEmail_request(token):
    '''Обрабатывает запрос на изменения email.'''
    if current_user.change_email(token):
        db.session.commit()
        flash(category='success', message='Ваш email адрес обновлён.')
        return redirect(url_for('user.editAccount_page', username=current_user.name))
    else:
        flash(category='error', message='Неверный запрос.')
        return redirect(url_for('user.editAccount_page', username=current_user.name))



@user.route(rule='/follow/<user_id>')
@login_required
def follow_request(user_id):
    '''Обрабатывает запрос на подписку'''
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        flash(category='error', message='Недействительный пользователь.')
        return redirect(url_for('main.home_page'))
    if current_user.is_following(user):
        flash(category='warn', message='Вы уже читаете данного пользователя.')
        return redirect(url_for('user.profile_page', username=user.name))
    
    current_user.follow(user)
    user_settings = UserSettings.query.filter_by(state='custom', profile=user).first()
    if user_settings.follow_me:
        notice_title = 'На вас подписались'
        notice_body = '<a href="{}">{}</a> - подписался на вас.'.format(
            url_for('user.profile_page', username=current_user.name), current_user.name
        )
        notice = Notice(title=notice_title, body=notice_body, author=user)

        db.session.add(notice)
        db.session.commit()
    flash(category='success', message='Вы подписаны на {}'.format(user.name))
    return redirect(url_for('user.profile_page', username=user.name))



@user.route(rule='/unfollow/<user_id>')
@login_required
def unfollow_request(user_id):
    '''Обрабатывает отписку от пользователя'''
    user = User.query.filter_by(id=user_id).first()
    if not current_user.is_following(user):
        flash(category='warn', message='Вы уже отписаны.')
        return redirect(url_for('user.profile_page', username=user.name))
    current_user.unfollow(user)

    user_settings = UserSettings.query.filter_by(state='custom', profile=user).first()
    if user_settings.unfollow_me:
        notice_title = 'От вас отписались'
        notice_body = '<a href="{}">{}</a> - отписался от вас.'.format(
            url_for('user.profile_page', username=current_user.name), current_user.name
        )
        notice = Notice(title=notice_title, body=notice_body, author=user)

        db.session.add(notice)
        db.session.commit()

    flash(category='success', message='Вы отписаны от {}'.format(user.name))
    return redirect(request.cookies.get('current_page'))



@user.route(rule='/unsubscribe/<user_id>')
@login_required
def unsubscribe_request(user_id):
    '''Реализовывает возможность текущему пользователю отписывать тех
    кто на него подписан'''
    user = User.query.filter_by(id=user_id).first()
    user.unfollow(current_user)

    user_settings = UserSettings.query.filter_by(state='custom', profile=user).first()
    if user_settings.unsubscribe_me:
        notice_title = 'Вас удалили из подписчиков'
        notice_body = '<a href="{}">{}</a> - удалил вас из подписчиков.'.format(
            url_for('user.profile_page', username=current_user.name), current_user.name
        )
        notice = Notice(title=notice_title, body=notice_body, author=user)

        db.session.add(notice)
        db.session.commit()

    flash(category='success', message='Вы удалили {} из ваших подписчиков'.format(user.name))
    return redirect(request.cookies.get('current_page'))
