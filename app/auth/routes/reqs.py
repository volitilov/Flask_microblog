# auth/routes/reqs.py

# Обрабатывает POST-запросы 
# Работа с данными: добавление, редактирование, удаление

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import redirect, url_for, flash, request
from flask_login import (
    login_required, current_user, logout_user, login_user
)

from .. import (
    # blueprint
    auth,

    # forms 
    PasswordResetRequest_form, PasswordReset_form,

    # models
    User, UserSettings,

    # database
    db,

    # email
    send_email,

    # utils
    create_response
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@auth.before_app_request
def before_request():
    '''Перехватывает запросы и фильтрует неподтверждённые учетные запеси, 
    если выполняются следующие условия:
    - пользователь был аутентифицирован;
    - учетная запись не потвеждена;
    - конечная точка запроса находится за пределами макета аутентификации.
    Если все условия выполняются, производится переадрисация на 
    auth/unconfirmed, для потверждения учетной записи.'''
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
            and request.endpoint \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
                return redirect(url_for('auth.unconfirmed_page'))



@auth.route(rule='/<username>/...logout')
@login_required
def logout_request(username):
    logout_user()
    flash(category='success', message='Вы успешно вышли')
    return redirect(url_for('main.home_page'))



@auth.route(rule='/confirm/<token>')
@login_required
def confirm_request(token):
    '''Подверждает учетную запись.
    Функция сначала проверяет, подтверждал ли прежде этот пользователь свою
    учетную запись, и если подтверждал - переадрисует его на главную страницу.'''
    if current_user.confirmed:
        return redirect(url_for('main.home_page'))
    if current_user.confirm(token):
        u_default_settings = UserSettings(state="default", profile=current_user)
        u_custom_settings = UserSettings(state="custom", profile=current_user)
        db.session.add_all([current_user, u_default_settings, u_custom_settings])
        db.session.commit()
        flash('Вы успешно подтвердили свой аккаунт.')
    else:
        flash('Ваша ссылка не действительна либо истекло время ссылки.')
    return redirect(url_for('main.home_page'))



@auth.route(rule='/confirm')
@login_required
def resendConfirmation_request():
    '''Делает повторную отправку письма со сылкой для потверждения'''
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Потверждение учетной записи', 'mail/auth/confirm/confirm', 
        user=current_user, token=token)
    flash('Новое электронное письмо с подтверждением отправлено вам на почтовый ящик.')
    return redirect(url_for('main.home_page'))

