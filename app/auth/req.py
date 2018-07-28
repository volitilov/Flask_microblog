# auth/req.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import redirect, url_for, flash, request, current_app

# app modules
from . import auth
from .forms import PasswordResetRequest_form, PasswordReset_form
from .. import db
from ..models.user import User
from ..models.user_settings import UserSettings
from ..email import send_email
from ..utils import create_response

# installed modules
from flask_login import login_required, current_user, logout_user

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@auth.before_app_request
def before_request():
	'''Перехватывает запросов и фильтрация неподтверждённых учетных
	запесей, перехватывает запросы если выполняются следующие условия:
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



@auth.route(rule='/...reset_password', methods=['POST'])
def resetPassword_request():
	'''Генерирует страницу запроса для сброса пароля'''
	form = PasswordResetRequest_form()

	if not current_user.is_anonymous:
		return redirect(url_for('main.home_page'))
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			token = user.generate_resetPassword_token()
			send_email(user.email, 'Сброс пароля', 'mail/auth/reset_password/reset', 
			user=user, token=token, next=request.args.get('next'))
		flash('Письмо для сброса пароля было отправленно вам на почтовый ящик.')
		return redirect(url_for('auth.login_page'))

