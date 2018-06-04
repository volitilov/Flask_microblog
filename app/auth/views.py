# auth/views.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import (
	render_template, redirect, url_for, flash, request, session, 
	current_app
)

# app modules
from . import auth
from .forms import (
	Login_form, Registration_form, PasswordResetRequest_form, 
	PasswordReset_form
)
from .. import db
from ..models.user import User
from ..email import send_email
from ..utils import create_response

# installed modules
from flask_login import (
	login_user, login_required, current_user, logout_user, login_url
)

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



@auth.route(rule='/login', methods=['GET', 'POST'])
def login_page():
	form = Login_form()
	data = {
		'form': form,
		'page_title': 'Страница авторизации.'
	}

	if form.validate_on_submit():
		email = form.email.data
		password = form.password.data
		remember_me = form.remember_me.data

		user = User.query.filter_by(email=email).first()
		if user is not None and user.verify_password(password):
			login_user(user, remember_me)
			next = request.cookies.get('next')
			if next is None:
				next = url_for('main.home_page')
			return redirect(next)

		flash('Неправильное имя пользователя или пароль.')

	return create_response(template='auth/login.html', data=data)



@auth.route(rule='/logout')
@login_required
def logout_page():
	logout_user()
	flash('You have been logged out')
	return redirect(url_for('main.home_page'))



@auth.route(rule='/register', methods=['GET', 'POST'])
def registration_page():
	form = Registration_form()
	data = {
		'form': form,
		'page_title': 'Страница регистрации.'
	}

	if form.validate_on_submit():
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

		return redirect(url_for('auth.login_page'))

	return create_response(template='auth/registr.html', data=data)



@auth.route(rule='/confirm/<token>')
@login_required
def confirm(token):
	'''Подверждает учетную запись.
	Функция сначала проверяет, подтверждал ли прежде этот пользователь свою
	учетную запись, и если подтверждал - переадрисует его на главную страницу.'''
	if current_user.confirmed:
		return redirect(url_for('main.home_page'))
	if current_user.confirm(token):
		db.session.add(current_user)
		db.session.commit()
		flash('You have confirmed your account')
	else:
		flash('Ваша ссылка не действительна либо истекло время ссылки.')
	return redirect(url_for('main.home_page'))



@auth.route(rule='/unconfirmed')
def unconfirmed_page():
	data = {
		'page_title': 'Страница с предложением потвердить свою учетную запись'
	}
	'''Генерирует страницу с предложением потвердить свою учетную запись'''
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for('main.home_page'))
	return create_response(template='auth/unconfirmed.html', data=data)



@auth.route(rule='/confirm')
@login_required
def resend_confirmation():
	'''Делает повторную отправку письма со сылкой для потверждения'''
	token = current_user.generate_confirmation_token()
	send_email(current_user.email, 'Потверждение учетной записи', 'mail/auth/confirm/confirm', 
		user=current_user, token=token)
	flash('Новое электронное письмо с подтверждением отправлено вам на почтовый ящик.')
	return redirect(url_for('main.home_page'))



@auth.route(rule='/reset_password', methods=['GET', 'POST'])
def passwordResetRequest_page():
	'''Генерирует страницу запроса для сброса пароля'''
	form = PasswordResetRequest_form()
	data = {
		'page_title': 'Страница запроса на сброс пароля',
		'form': form
	}
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
	return create_response(template='auth/reset_password_request.html', data=data)



@auth.route(rule='/reset/<token>', methods=['GET', 'POST'])
@login_required
def passwordReset_page(token):
	'''Обрабатывает запрос на изменения пароля'''
	form = PasswordReset_form()
	data = {
		'page_title': 'Страница запроса на сброс пароля',
		'form': form
	}
	if not current_user.is_anonymous:
		return redirect(url_for('main.home_page'))
	if form.validate_on_submit():
		if User.reset_password(token, form.password.data):
			db.session.commit()
			flash('Ваш пароль успешно изменён.')
			return redirect(url_for('auth.login'))
		else:
			return redirect(url_for('main.home_page'))
	return create_response(template='auth/reset_password.html', data=data)

