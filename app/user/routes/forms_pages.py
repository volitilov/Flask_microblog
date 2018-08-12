# user/routes/forms_pages.py

# Обрабатывает страницы с формами

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

import os
from flask import redirect, request, url_for, flash, session, current_app
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
    create_response,

    # database
    db,

    # data
    page_titles
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@user.route(rule='/<username>/settings/profile', methods=['GET', 'POST'])
@login_required
def editProfile_page(username):
    '''Генерирует и обрабатывает страницу настроек пользователя'''
    form = EditProfile_form()
    upload_folder = current_app.config['UPLOAD_FOLDER']
    allowed_extensions = current_app.config['ALLOWED_EXTENSIONS']
    user = User.query.filter_by(name=username).first()

    first_name = form.first_name.data
    last_name = form.last_name.data
    about = form.about.data
    location = form.location.data
    photo = form.photo.data


    if form.validate_on_submit():
        if photo:
            filename = secure_filename(photo.filename)
            _, ext = os.path.splitext(filename)
            if ext in allowed_extensions:
                new_file_url = os.path.join(upload_folder, 'photos', filename)
                old_file_url = os.path.join(upload_folder, user.photo_url)

                os.remove(old_file_url)
                if os.path.isfile(new_file_url):
                    os.remove(new_file_url)
                    
                photo.save(new_file_url)

                user.photo_url = 'photos/' + filename
            else:
                return redirect(url_for('user.editProfile_page', username=username))

        user.first_name = first_name
        user.last_name = last_name
        user.about_me = about
        user.location = location

        db.session.add(user)
        db.session.commit()
        
        flash(message='Новые данные сохранены.', category='success')
        return redirect(url_for('user.editProfile_page', username=username))
    
    form.about.data = user.about_me
    
    return create_response(template='edit_profile.html', data={
        'page_title': page_titles['editProfile_page'],
        'page': 'edit_profile',
        'form': form
    })



@user.route(rule='/<username>/settings/accout/change_login', methods=['GET','POST'])
@fresh_login_required
def changeLogin_page(username):
    '''Генерирует и обрабатывает страницу изменения логина'''
    form = ChangeLogin_form()

    if form.validate_on_submit():
        name = form.name.data
        current_user.name = name
        db.session.add(current_user)
        db.session.commit()
        flash(category='success', message='Ваш login успешно изменён.')
        return redirect(url_for('user.editAccount_page', username=current_user.name))
    
    return create_response(template='change_login.html', data={
        'page_title': page_titles['changeLogin_page'],
        'form': form
    })



@user.route(rule='/<username>/settings/account/change_password', methods=['GET','POST'])
@fresh_login_required
def changePassword_page(username):
    '''Генерирует и обрабатывает страницу изменения пароля'''
    form = ChangePassword_form()

    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data

            db.session.add(current_user)
            db.session.commit()
            flash(category='success', message='Ваш пароль успешно изменён.')
            return redirect(url_for('user.editAccount_page', username=current_user.name))
        else:
            flash(category='error', message='Неверный пароль.')
            return redirect(url_for('user.changePassword_page', username=current_user.name))

    return create_response(template='change_password.html', data={
        'page_title': page_titles['changePassword_page'],
        'form': form
    })



@user.route(rule='/<username>/settings/account/change_email', methods=['GET','POST'])
@fresh_login_required
def changeEmail_page(username):
    '''Генерирует и обрабатывает страницу изменения email'''
    form = ChangeEmail_form()
    new_email = form.email

    if form.validate_on_submit():
        form.validate_email(new_email)
        current_user.email = new_email.data
        token = current_user.generate_changeEmail_token(new_email.data)
        send_email(new_email, 'Потвердите свой email адрес', 
            'mail/confirm_email/index', user=current_user, token=token)
        flash(message='''На ваш новый почтовый адрес отправленно письмо с инструкциями,
                для потверждения нового адреса''')
        return redirect(url_for('user.editAccount_page', username=current_user.name))
    
    return create_response(template='change_email.html', data={
        'page_title': page_titles['changeEmail_page'],
        'form': form
    })



@user.route('/<username>/settings/notice', methods=['GET', 'POST'])
@login_required
def editNotice_page(username):
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



@user.route('/<username>/admin/comments/<int:id>/...return', methods=['GET', 'POST'])
@login_required
def adminReturnComment_page(username, id):
    '''Генерирует и обрабатывает страницу возврата комментария на доработку'''
    form = AddNotice_form()
    comment = Comment.query.get_or_404(id)

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

    posts = Post.query.filter_by(state='moderation')
    comments = []
    for i in current_user.posts:
        com = i.comments.filter_by(state='moderation')
        comments.extend(com)

    return create_response(template='admin/noticeComment_form.html', data={
        'title_page': page_titles['adminReturnComment_page'],
        'form': form,
        'comment': comment,
        'posts': posts,
        'comments': comments
    })

