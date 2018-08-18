# user/routes/forms_pages.py

# Обрабатывает запросы от форм

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

import os
from flask import (
    redirect, request, url_for, flash, session, current_app, jsonify
)
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required, fresh_login_required

from .. import (
    # blueprint
    user,

    # forms
    EditProfile_form, ChangeEmail_form, ChangeLogin_form, 
    ChangePassword_form, EditNotice_form, AddNotice_form,

    # models
    User, Post, Notice, Comment, UserSettings,

    # email
    send_email,

    # utils
    create_response, flash_errors,

    # database
    db,

    # data
    page_titles
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@user.route(rule='/settings/profile', methods=['POST'])
@login_required
def editProfileForm_req():
    '''Генерирует и обрабатывает страницу настроек пользователя'''
    form = EditProfile_form()
    upload_folder = current_app.config['UPLOAD_FOLDER']

    if form.validate():
        first_name = form.first_name.data
        last_name = form.last_name.data
        about = form.about.data
        location = form.location.data
        photo = form.file_photo.data

        if photo:
            filename = secure_filename(photo.filename)
            new_file_url = os.path.join(upload_folder, 'photos', filename)
            old_file_url = os.path.join(upload_folder, current_user.photo_url)

            os.remove(old_file_url)
            if os.path.isfile(new_file_url):
                os.remove(new_file_url)
                
            photo.save(new_file_url)

            current_user.photo_url = 'photos/' + filename

        current_user.first_name = first_name
        current_user.last_name = last_name
        current_user.about_me = about
        current_user.location = location

        db.session.add(current_user)
        db.session.commit()
        
        flash(message='Новые данные сохранены.', category='success')
        return jsonify({'next_url': url_for('user.profile_page', username=current_user.name)})
    
    return jsonify({'errors': flash_errors(form)})



@user.route(rule='/settings/accout/change_login', methods=['POST'])
@fresh_login_required
def changeLoginForm_req():
    '''Генерирует и обрабатывает страницу изменения логина'''
    form = ChangeLogin_form()

    if form.validate():
        name = form.name.data
        current_user.name = name
        db.session.add(current_user)
        db.session.commit()
        flash(category='success', message='Ваш login успешно изменён.')
        return jsonify({'next_url': url_for('user.editAccount_page')})
    
    return jsonify({'errors': flash_errors(form)})



@user.route(rule='/settings/account/change_password', methods=['POST'])
@fresh_login_required
def changePasswordForm_req():
    '''Генерирует и обрабатывает страницу изменения пароля'''
    form = ChangePassword_form()

    if form.validate():
        current_user.password = form.password.data

        db.session.add(current_user)
        db.session.commit()
        flash(category='success', message='Ваш пароль успешно изменён.')
        return jsonify({'next_url': url_for('user.editAccount_page')})

    return jsonify({'errors': flash_errors(form)})



@user.route(rule='/settings/account/change_email', methods=['POST'])
@fresh_login_required
def changeEmailForm_req():
    '''Генерирует и обрабатывает страницу изменения email'''
    form = ChangeEmail_form()

    if form.validate():
        current_user.email = form.email.data
        token = current_user.generate_changeEmail_token(form.email.data)
        send_email(form.email.data, 'Потвердите свой email адрес', 
            'mail/confirm_email/index', user=current_user, token=token)
        flash(message='''На ваш новый почтовый адрес отправленно письмо с инструкциями,
                для потверждения нового адреса''')
        return jsonify({'next_url': url_for('user.editAccount_page', username=current_user.name)})
    
    return jsonify({'errors': flash_errors(form)})



@user.route('/settings/notice', methods=['GET', 'POST'])
@login_required
def editNotice_page():
    '''Генерирует и обрабатывает страницу настроек уведомлений'''
    form = EditNotice_form()

    if form.validate_on_submit():
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

    user_settings = UserSettings.query.filter_by(state='custom', profile=current_user).first()

    form.comments_me.data = user_settings.comments_me
    form.follow_me.data = user_settings.follow_me
    form.unfollow_me.data = user_settings.unfollow_me
    form.unsubscribe_me.data = user_settings.unsubscribe_me
    form.comment_moderated.data = user_settings.comment_moderated
    form.post_moderated.data = user_settings.post_moderated

    return create_response(template='edit_notice.html', data={
        'page_title': page_titles['editNotice_page'],
        'page': 'edit_notice',
        'form': form
    })



@user.route('/admin/comments/<int:id>/...return', methods=['POST'])
@login_required
def adminReturnCommentForm_req(id):
    '''Генерирует и обрабатывает страницу возврата комментария на доработку'''
    form = AddNotice_form()
    comment = Comment.query.get_or_404(id)

    if form.validate():
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
        return jsonify({'next_url': url_for('user.adminComments_page', username=current_user.name)})

    return jsonify({'errors': flash_errors(form)})

