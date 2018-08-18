# auth/routes/forms_pages.py

# Обрабатывает запросы от форм

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_user, login_required, current_user

from .. import (
    # blueprint
    auth,

    # forms
    Login_form, Registration_form, PasswordReset_form, 
    PasswordResetRequest_form,

    # models 
    User,

    # database
    db,

    # email
    send_email,

    # utils
    flash_errors
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@auth.route(rule='/login_form_request', methods=['POST'])
def loginForm_req():
    '''Обрабатывает запрос на авторизацию'''
    form = Login_form()

    if form.validate():
        email = form.email.data
        password = form.password.data
        remember_me = form.remember_me.data

        user = User.query.filter_by(email=email).first()
        if user.verify_password(password):
            login_user(user, remember_me)
            next = request.cookies.get('next')
            if next is None:
                next = url_for('main.home_page')
            flash(category='success', message='Вы успешно авторизовались')
            return jsonify({'next_url': next})
        else:
            return jsonify({
                'errors': flash_errors(form),
                'flash': {'category': 'error', 'message': 'Пароль не подходит к данному email'}
            })

    return jsonify({'errors': flash_errors(form)})



@auth.route(rule='/registration_form_request', methods=['POST'])
def registrationForm_req():
    '''Генерирует страницу регистрации'''
    form = Registration_form()
    # recaptcha_private_key = current_app.config['RECAPTCHA_PRIVATE_KEY']

    if form.validate():
        # response = request.form.get('g-recaptcha-response')
        # if check_recaptcha(response, recaptcha_private_key):
        username = form.username.data
        email = form.email.data
        password = form.password.data

        user = User(name=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        token = user.generate_confirmation_token()
        send_email(user.email, 'Потверждение учетной записи', 'mail/auth/confirm/confirm', 
            user=user, token=token)
        flash('Письмо для подтверждения регистрации отправленно, на почтовый ящик')

        return jsonify({
            'next_url': url_for('auth.login_page')
        })

    return jsonify({'errors': flash_errors(form)})



@auth.route(rule='/password_reset/<token>', methods=['POST'])
def passwordResetForm_req(token):
    '''Обрабатывает запрос на изменения пароля'''
    form = PasswordReset_form()

    if not current_user.is_anonymous:
        return redirect(url_for('main.home_page'))
    if form.validate():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('Ваш пароль успешно изменён.')
            return jsonify({'next_url': url_for('auth.login_page')})
        else:
            return jsonify({
                'flash': {'category': 'error', 'message': 'Токен не действителен, попробуйте снова.'}
            })
    return jsonify({'errors': flash_errors(form)})



@auth.route(rule='/...reset_password', methods=['POST'])
def resetPasswordForm_req():
    '''Генерирует страницу запроса для сброса пароля'''
    form = PasswordResetRequest_form()

    if not current_user.is_anonymous:
        return redirect(url_for('main.home_page'))
    if form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_resetPassword_token()
            send_email(user.email, 'Сброс пароля', 'mail/auth/reset_password/reset', 
            user=user, token=token, next=request.args.get('next'))
            flash('Письмо для сброса пароля было отправленно вам на почтовый ящик.')
            return jsonify({'next_url': url_for('auth.login_page')})
        else:
            return jsonify({
                'flash': {'category': 'error', 'message': 'Данный email не зарегестрирован'}
            })

    return jsonify({'errors': flash_errors(form)})

