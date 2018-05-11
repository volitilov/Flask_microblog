# auth/views.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import (
	render_template, redirect, url_for, flash, request
)

# app modules
from . import auth
from .forms import (
	Login_form, Registration_form, PasswordResetRequest_form, 
	PasswordReset_form, ChangeEmail_form, ChangeLogin_form,
	ChangePassword_form
)
from .. import db
from ..models import User
from ..email import send_email

# installed modules
from flask_login import (
	login_user, login_required, current_user, logout_user
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
	if current_user.is_authenticated \
		and not current_user.confirmed \
		and request.endpoint \
		and request.endpoint[:5] != 'auth.' \
		and request.endpoint != 'static':
			return redirect(url_for('auth.unconfirmed_page'))



@auth.route('/login', methods=['GET', 'POST'])
def login_page():
	form = Login_form(request.form)
	data = {
		'form': form,
		'page_title': 'Страница авторизации.'
	}


	if form.validate():
		email = form.email.data
		password = form.password.data
		remember_me = form.remember_me.data

		user = User.query.filter_by(email=email).first()
		if user is not None and user.verify_password(password):
			login_user(user, remember_me)
			return redirect(request.args.get('next') or url_for('main.home_page'))

		flash('Неправильное имя пользователя или пароль.')

	return render_template('auth/login.html', data=data)



@auth.route('/change_login', methods=['POST', 'GET'])
def changeLogin_page():
	form = ChangeLogin_form(request.form)
	data = {
		'page_title': 'Страница изменения логина',
		'form': form
	}

	if form.validate():
		current_user.name = form.name.data

		flash('Ваш login успешно изменён.')
		db.session.add(current_user)
		db.session.commit()
		return redirect(url_for('main.home_page'))

	return render_template('auth/change-login.html', data=data)



@auth.route('/logout')
@login_required
def logout_page():
	logout_user()
	flash('Вы вышли из системы.')
	return redirect(url_for('main.home_page'))



@auth.route('/register', methods=['GET', 'POST'])
def registration_page():
	form = Registration_form(request.form)
	data = {
		'form': form,
		'page_title': 'Страница регистрации.'
	}

	if form.validate():
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

		return redirect(url_for('auth.login'))

	return render_template('auth/registr.html', data=data)



@auth.route('/confirm/<token>')
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
		flash('Ваш аккаунт потверждён спосибо!')
	else:
		flash('Ваша ссылка не действительна либо истекло время ссылки.')
	return redirect(url_for('main.home_page'))



@auth.route('/unconfirmed')
def unconfirmed_page():
	data = {
		'page_title': 'Страница с предложением потвердить свою учетную запись'
	}
	'''Генерирует страницу с предложением потвердить свою учетную запись'''
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for('main.home_page'))
	return render_template('auth/unconfirmed.html', data=data)



@auth.route('/confirm')
@login_required
def resend_confirmation():
	'''Делает повторную отправку письма со сылкой для потверждения'''
	token = current_user.generate_confirmation_token()
	send_email(current_user.email, 'Потверждение учетной записи', 'mail/auth/confirm/confirm', 
		user=current_user, token=token)
	flash('Новое электронное письмо с подтверждением отправлено вам на почтовый ящик.')
	return redirect(url_for('main.home_page'))



@auth.route('/reset_password', methods=['GET', 'POST'])
def passwordResetRequest_page():
	'''Генерирует страницу запроса для сброса пароля'''
	form = PasswordResetRequest_form(request.form)
	data = {
		'page_title': 'Страница запроса на сброс пароля',
		'form': form
	}
	if not current_user.is_anonymous:
		return redirect(url_for('main.home_page'))
	if form.validate():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			token = user.generate_resetPassword_token()
			send_email(user.email, 'Сброс пароля', 'mail/auth/reset_password/reset', 
			user=user, token=token, next=request.args.get('next'))
		flash('Письмо для сброса пароля было отправленно вам на почтовый ящик.')
		return redirect(url_for('auth.login'))
	return render_template('auth/reset_password_request.html', data=data)



@auth.route('/reset/<token>', methods=['GET', 'POST'])
@login_required
def passwordReset_page(token):
	'''Обрабатывает запрос на изменения пароля'''
	form = PasswordReset_form(request.form)
	data = {
		'page_title': 'Страница запроса на сброс пароля',
		'form': form
	}
	if not current_user.is_anonymous:
		return redirect(url_for('main.home_page'))
	if form.validate():
		if User.reset_password(token, form.password.data):
			db.session.commit()
			flash('Ваш пароль успешно изменён.')
			return redirect(url_for('auth.login'))
		else:
			return redirect(url_for('main.home_page'))
	return render_template('auth/reset_password.html', data=data)



@auth.route('/change_password', methods=['POST', 'GET'])
def changePassword_page():
	form = ChangePassword_form(request.form)
	data = {
		'page_title': 'Страница изменения пароля',
		'form': form
	}

	if form.validate():
		if current_user.verify_password(form.old_password.data):
			current_user.password = form.password.data

			flash('Ваш пароль успешно изменён.')
			db.session.add(current_user)
			db.session.commit()
			return redirect(url_for('main.home_page'))

	return render_template('auth/change-password.html', data=data)



@auth.route('/change_email', methods=['POST', 'GET'])
def changeEmailRequest_page():
	'''Генерирует страницу запроса на изменения email'''
	form = ChangeEmail_form(request.form)
	new_email = form.email.data
	data = {
		'page_title': 'Страница запроса на изменения email',
		'form': form
	}
	if form.validate():
		if current_user.verify_password(form.password.data):
			current_user.email = new_email
			token = current_user.generate_changeEmail_token(new_email)
			send_email(new_email, 'Потвердите свой email адрес', 
				'mail/auth/change_email/index', user=current_user, token=token)
			flash('''На ваш новый почтовый адрес отправленно письмо с инструкциями,
					для потверждения нового адреса''')
			return redirect(url_for('main.home_page'))
		else:
			flash('Неверный пароль')

	return render_template('auth/change_email.html', data=data)



@auth.route('/change_email/<token>', methods=['POST', 'GET'])
@login_required
def changeEmail(token):
	'''Обрабатывает запрос на изменения email.'''
	if current_user.change_email(token):
		db.session.commit()
		flash('Ваш email адрес обновлён.')
	else:
		flash('Неверный запрос.')
	return redirect(url_for('main.home_page'))
