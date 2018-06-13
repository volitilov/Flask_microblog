# user/views.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

import os

from flask import (
	render_template, redirect, request, url_for, flash, session, abort,
	current_app, send_from_directory
)
from werkzeug.utils import secure_filename

# flask extensions
from flask_login import current_user, login_required, fresh_login_required

# 
from . import user
from .forms import (
	EditProfile_form, ChangeEmail_form, ChangeLogin_form, 
	ChangePassword_form
)
from ..models.user import User
from ..email import send_email
from ..utils import create_response
from .. import db

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@user.route(rule='/users/<username>')
def profile_page(username):
	'''Генерирует страницу профиля пользователя.'''
	return create_response(template='user/profile.html', data={
		'page_title': 'Страница профиля',
		'user': User.query.filter_by(name=username).first_or_404()
	})



@user.route(rule='/users/settings/profile', methods=['GET', 'POST'])
@fresh_login_required
def editProfile_page():
	'''Генерирует страницу настроек пользователя'''
	form = EditProfile_form()
	upload_folder = current_app.config['UPLOAD_FOLDER']
	allowed_extensions = current_app.config['ALLOWED_EXTENSIONS']
	bro = User.query.filter_by(name=current_user.name).first()

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
				photo_base_url = os.path.join(upload_folder, 'photos', filename)
				photo.save(photo_base_url)

				bro.photo_url = 'photos/' + filename
			else:
				flash('Поддерживаются только следующие форматы: png, jpg, jpeg, gif')
				return redirect(url_for('user.editProfile_page'))

		bro.first_name = first_name
		bro.last_name = last_name
		bro.about_me = about
		bro.location = location

		db.session.add(bro)
		db.session.commit()
		
		flash('Новые данные сохранены.')
		return redirect(url_for('user.editProfile_page'))

	
	return create_response(template='user/edit_profile.html', data={
		'page_title': 'Страница редактирования профиля',
		'form': form
	})



@user.route(rule='/users/settings/account')
@fresh_login_required
def editAccount_page():
	changeLogin_form = ChangeLogin_form()
	changePassword_form = ChangePassword_form()
	changeEmail_form = ChangeEmail_form()

	return create_response(template='user/edit_account.html', data={
		'page_title': 'Страница редактирования аккаунта',
		'login_form': changeLogin_form,
		'password_form': changePassword_form,
		'email_form': changeEmail_form
	})



@user.route(rule='/change_login', methods=['POST'])
@fresh_login_required
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
@fresh_login_required
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
@fresh_login_required
def changeEmail(token):
	'''Обрабатывает запрос на изменения email.'''
	if current_user.change_email(token):
		db.session.commit()
		flash('Ваш email адрес обновлён.')
		return redirect(url_for('user.editAccount_page'))
	else:
		flash('Неверный запрос.')
		return redirect(url_for('user.editAccount_page'))
	


@user.route(rule='/follow/<user_id>')
@fresh_login_required
def follow(user_id):
	user = User.query.filter_by(id=user_id).first()
	if user is None:
		flash('Недействительный пользователь.')
		return redirect(url_for('main.home_page'))
	if current_user.is_following(user):
		flash('Вы уже читаете данного пользователя.')
		return redirect(url_for('user.profile_page', username=user.name))
	current_user.follow(user)
	flash('Вы подписаны на {}'.format(user.name))
	return redirect(url_for('user.profile_page', username=user.name))



@user.route(rule='/unfollow/<user_id>')
@fresh_login_required
def unfollow(user_id):
	user = User.query.filter_by(id=user_id).first()
	print(current_user.is_following(user))
	if user is None:
		flash('Недействительный пользователь.')
		return redirect(url_for('main.home_page'))
	if not current_user.is_following(user):
		flash('Вы уже отписаны.')
		return redirect(url_for('user.profile_page', username=user.name))
	current_user.unfollow(user)
	flash('Вы отписаны от {}'.format(user.name))
	return redirect(url_for('user.profile_page', username=user.name))



@user.route(rule='/users/followers/<user_id>')
def followers_page(user_id):
	user = User.query.filter_by(id=user_id).first()
	if user is None:
		flash('Недействительный пользователь.')
		return redirect(url_for('main.home_page'))
	page = request.args.get('page', 1, type=int)
	pagination = user.followers.paginate(
		page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
		error_out=False)
	follows = [{'user': item.follower, 'timestamp': item.timestamp} 
				for item in pagination.items] 

	return create_response(template='user/followers.html', data={
		'page_title': 'Страница подписчиков.',
		'user': user,
		'pagination': pagination,
		'follows': follows,
		'endpoint': 'user.followers_page',
		'title': 'Всего подписчиков: {}'.format(user.followers.count() - 1)
	})



@user.route(rule='/users/followed_by/<user_id>')
def followedBy_page(user_id):
	user = User.query.filter_by(id=user_id).first()
	if user is None:
		flash('Недействительный пользователь.')
		return redirect(url_for('main.home_page'))
	page = request.args.get('page', 1, type=int)
	pagination = user.followed.paginate(
		page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
		error_out=False)
	follows = [{'user': item.followed, 'timestamp': item.timestamp} 
				for item in pagination.items]

	return create_response(template='user/followers.html', data={
		'page_title': 'Страница подписок.',
		'user': user,
		'pagination': pagination,
		'follows': follows,
		'endpoint': 'user.followedBy_page',
		'title': 'Всего подписан на: {}'.format(user.followed.count() - 1)
	})


@user.route(rule='/delete_account', methods=['POST'])
@fresh_login_required
def deleteAccount_request():
	user = User.query.get(current_user.id)
	for post in user.posts:
		db.session.delete(post)
	for comment in user.comments:
		db.session.delete(comment)
		
	db.session.delete(user)
	db.session.commit()
	return redirect(url_for('main.home_page'))
