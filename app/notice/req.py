#! notice/req.py

#

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import redirect, url_for, flash, current_app, jsonify
from flask_login import current_user, login_required

from . import notice
from .forms import AddNotice_form
from ..models.notice import Notice
from ..models.user import User
from ..models.user_settings import UserSettings
from ..models.role import Role
from .. import db

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


@notice.route('/notice/...add', methods=['POST'])
@login_required
def addNotice_request():
    form = AddNotice_form()

    if form.validate_on_submit():
        body = form.body.data

        user_role = Role.query.filter_by(name='Admin').first()
        users = User.query.filter(User.role!=user_role).all()
        notice_list = []

        for user in users:
            notice = Notice(body=body, author=user, title='admin')
            notice_list.append(notice)

        db.session.add_all(notice_list)
        db.session.commit()

        flash(message='Ваше уведомление отправленно', category='success')
        return redirect(url_for('notice.addNotice_page', username=current_user.name))
    else:
        flash(category='error', message='Ваши данные ошибочны')
        return redirect(url_for('notice.addNotice_page', username=current_user.name))



@notice.route('/<username>/notice/<int:id>/...del', methods=['POST'])
@login_required
def deleteNotice_request(username, id):
    notice = Notice.query.get_or_404(id)
   
    if current_user == notice.author:
        db.session.delete(notice)
        db.session.commit()
    else:
        flash(category='warn', 
            message='Вы не можите удалить уведомление, так как не являетесь его владельцом')
        return jsonify({
            'success': False
        })
    
    return jsonify({
        'success': True
    })
