#! notice/req.py

#

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import redirect, url_for, flash, current_app
from flask_login import current_user, login_required

from . import notice
from .forms import AddNotice_form, SettingsNotice_form
from ..models.notice import Notice
from ..models.user import User
from ..models.user_settings import UserSettings
from ..models.role import Role
from .. import db

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


@notice.route('/...add', methods=['POST'])
@login_required
def addNotice_request():
    form = AddNotice_form()
    client = current_app.memory

    if form.validate_on_submit():
        body = form.body.data

        user_role = Role.query.filter_by(name='User').first()
        users = User.query.filter_by(role=user_role).all()
        notice_list = []

        for i in users:
            notice = Notice(body=body, author=i)
            notice_list.append(notice)

        db.session.add_all(notice_list)
        db.session.commit()

        res = int(client.get(key='notice_count'))
        res += 1
        client.set(key='notice_count', value=res)

        flash(message='Ваше уведомление отправленно', category='success')
        return redirect(url_for('notice.addNotice_page'))
    else:
        flash(category='error', message='Ваши данные ошибочны')
        return redirect(url_for('notice.addNotice_page'))



@notice.route('/<int:id>/...del', methods=['POST'])
@login_required
def deleteNotice_request(id):
    notice = Notice.query.get_or_404(id)
   
    if current_user == notice.author:
        db.session.delete(notice)
        db.session.commit()
    else:
        flash(category='warn', 
            message='Вы не можите удалить уведомление, так как не являетесь его владельцом')

    return redirect(url_for('notice.notice_page', username=current_user.name))



@notice.route('/...change_settings', methods=['POST'])
@login_required
def changeSettings_request():
    form = SettingsNotice_form()
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
    return redirect(url_for('notice.noticeSettings_page'))



@notice.route('/...returnDefault_settings')
@login_required
def returnDefaultSettings_request():
    form = SettingsNotice_form()
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
    return redirect(url_for('notice.noticeSettings_page'))