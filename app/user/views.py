# user/views.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import (
	render_template, redirect, request, url_for, flash, session, abort
)

# flask extensions
from flask_login import current_user, login_required

# 
from . import user
from .forms import (
	EditProfile_form, ChangeEmail_form, ChangeLogin_form, 
	ChangePassword_form
)
from ..models import Post, User
from ..email import send_email
from ..utils import create_response
from .. import db

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@user.route(rule='/users/<username>')
def profile_page(username):
	'''Генерирует страницу профиля пользователя.'''
	user = User.query.filter_by(name=username).first_or_404()
	data = {
		'page_title': 'Страница профиля',
		'user': user
	}

	return create_response(template='user/profile.html', data=data)



@user.route(rule='/users/settings/profile', methods=['GET', 'POST'])
@login_required
def editProfile_page():
	'''Генерирует страницу настроек пользователя'''
	form = EditProfile_form()

	data = {
		'page_title': 'Страница редактирования профиля',
		'form': form
	}

	bro = User.query.filter_by(name=current_user.name).first()

	first_name = form.first_name.data
	last_name = form.last_name.data
	about = form.about.data
	location = form.location.data

	if form.validate_on_submit():
		bro.first_name = first_name
		bro.last_name = last_name
		bro.about_me = about
		bro.location = location
		db.session.add(bro)
		db.session.commit()
		
		flash('Новые данные сохранены.')
		return redirect(url_for('user.editProfile_page'))

	
	return create_response(template='user/edit_profile.html', data=data)



@user.route(rule='/users/settings/account')
@login_required
def editAccount_page():
	changeLogin_form = ChangeLogin_form()
	changePassword_form = ChangePassword_form()
	changeEmail_form = ChangeEmail_form()

	data = {
		'page_title': 'Страница редактирования аккаунта',
		'login_form': changeLogin_form,
		'password_form': changePassword_form,
		'email_form': changeEmail_form
	}
	return create_response(template='user/edit_account.html', data=data)



@user.route(rule='/change_login', methods=['POST'])
def changeLogin_request():
	form = ChangeLogin_form()

	if form.validate_on_submit():
		current_user.name = form.name.data

		flash('Ваш login успешно изменён.')
		db.session.add(current_user)
		db.session.commit()
		return redirect(url_for('user.editAccount_page'))
	else:
		flash('Неверные данные')




@user.route(rule='/change_password', methods=['POST'])
def changePassword_request():
	form = ChangePassword_form()

	if form.validate_on_submit():
		if current_user.verify_password(form.old_password.data):
			current_user.password = form.password.data

			flash('Ваш пароль успешно изменён.')
			db.session.add(current_user)
			db.session.commit()
			return redirect(url_for('user.editAccount_page'))
		else:
			flash('Неверный пароль.')
			return redirect(url_for('user.editAccount_page'))
	else:
		flash('Неверно заполнена форма.')
		return redirect(url_for('user.editAccount_page'))



@user.route(rule='/change_email', methods=['POST'])
def changeEmail_request():
	form = ChangeEmail_form()
	new_email = form.email.data

	if form.validate_on_submit():
		current_user.email = new_email
		token = current_user.generate_changeEmail_token(new_email)
		send_email(new_email, 'Потвердите свой email адрес', 
			'mail/confirm_email/index', user=current_user, token=token)
		flash('''На ваш новый почтовый адрес отправленно письмо с инструкциями,
				для потверждения нового адреса''')
		return redirect(url_for('user.editAccount_page'))
	else:
		flash('Неверно заполнена форма.')
		return redirect(url_for('user.editAccount_page'))



@user.route(rule='/change_email/<token>')
@login_required
def changeEmail(token):
	'''Обрабатывает запрос на изменения email.'''
	if current_user.change_email(token):
		db.session.commit()
		flash('Ваш email адрес обновлён.')
		return redirect(url_for('user.editAccount_page'))
	else:
		flash('Неверный запрос.')
		return redirect(url_for('user.editAccount_page'))