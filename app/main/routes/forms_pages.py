# main/routes/forms_pages.py

# Обрабатывает запросы от форм

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import redirect, url_for, flash, jsonify, current_app
from flask_login import current_user, login_required

from .. import (
    # blueprint
    main,

    # forms
    Search_form, Support_form,

    # utils
    flash_errors,

    # models
    User, Message,

    # database
    db
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@main.route('/posts/...search', methods=['POST'])
def searchForm_req():
    form = Search_form()

    if form.validate():
        return jsonify({
            'next_url': url_for('main.searchResults_page', data=form.q.data)
        })
        
    return jsonify({'errors': flash_errors(form)})



@main.route('/support', methods=['POST'])
@login_required
def supportForm_req():
    '''Обрабатывает запрос от формы службы поддержки'''
    form = Support_form()

    if form.validate():
        moderator = current_app.config['APP_MODERATOR']
        to = User.query.filter_by(email=moderator).first()

        message = Message(
            title = form.title.data,
            body = form.body.data,
            author = current_user,
            recipient=to)

        db.session.add_all([to, message])
        db.session.commit()

        flash(category='success', message='''Ваше сообщение отправленно. Ожидайте ответа
            мы пришлём вам уведомление.''')
        return jsonify({
            'next_url': url_for('main.home_page')
        })
        
    return jsonify({'errors': flash_errors(form)})
