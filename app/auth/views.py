# auth/views.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import (
	render_template, redirect, url_for, flash, request, current_app
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
	login_user, login_required, current_user, logout_user
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@auth.route(rule='/login', methods=['GET', 'POST'])
def login_page():
	form = Login_form()

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
			flash(message='Вы успешно авторизовались')
			return redirect(next)

		flash(message='Неправильное имя пользователя или пароль.', category='error')

	return create_response(template='auth/login.html', data={
		'form': form,
		'page_title': 'Страница авторизации.'
	})



@auth.route(rule='/register', methods=['GET', 'POST'])
def registration_page():
	form = Registration_form()
	recaptcha_private_key = current_app.config['RECAPTCHA_PRIVATE_KEY']
	data = {
		'form': form,
		'page_title': 'Страница регистрации.'
	}

	if form.validate_on_submit():
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

		return redirect(url_for('auth.login_page'))
	
	return create_response(template='auth/registr.html', data=data)



@auth.route(rule='/unconfirmed')
def unconfirmed_page():
	'''Генерирует страницу с предложением потвердить свою учетную запись'''
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for('main.home_page'))
	return create_response(template='auth/unconfirmed.html', data={
		'page_title': 'Страница с предложением потвердить свою учетную запись'
	})



@auth.route(rule='/reset_password')
def resetPassword_page():
	'''Генерирует страницу запроса для сброса пароля'''
	form = PasswordResetRequest_form()
	return create_response(template='auth/reset_password_request.html', data={
		'page_title': 'Страница запроса на сброс пароля',
		'form': form
	})



@auth.route(rule='/reset/<token>', methods=['GET', 'POST'])
def passwordReset_page(token):
	'''Обрабатывает запрос на изменения пароля'''
	form = PasswordReset_form()

	if not current_user.is_anonymous:
		return redirect(url_for('main.home_page'))
	if form.validate_on_submit():
		if User.reset_password(token, form.password.data):
			db.session.commit()
			flash('Ваш пароль успешно изменён.')
			return redirect(url_for('auth.login_page'))
		else:
			return redirect(url_for('main.home_page'))
	return create_response(template='auth/reset_password.html', data={
		'page_title': 'Страница изминения пароля',
		'form': form
	})

