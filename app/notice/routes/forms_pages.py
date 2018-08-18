# notice/routes/forms_pages.py

# Обрабатывает запросы от форм

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import flash, redirect, url_for, jsonify
from flask_login import login_required, current_user

from .. import (
    # blueprint
    notice,

    # forms
    AddNotice_form,

    # models
    Notice, Role, User,

    # database
    db,

    # utils
    flash_errors, is_admin
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@notice.route('/<username>/notice/add', methods=['POST'])
@is_admin
def addNoticeForm_req(username):
    '''Обрабатывает форму добавления уведомлений'''
    form = AddNotice_form()

    if form.validate():
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
        return jsonify({
            'next_url': url_for('notice.addNotice_page', username=current_user.name)
        }) 
    
    return jsonify({'errors': flash_errors(form)})