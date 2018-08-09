# notice/routes/forms_pages.py

# Обрабатывает страницы с формами

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import flash, redirect, url_for
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
    create_response
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@notice.route('/<username>/notice/add', methods=['GET', 'POST'])
@login_required
def addNotice_page(username):
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

    return create_response(template='add.html', data={
        'page_title': 'Страница создания уведомления',
        'form': form,
    })