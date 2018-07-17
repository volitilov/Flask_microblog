# user/views.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

import os

from flask import (
	render_template, redirect, request, url_for, flash, session, abort,
	current_app, send_from_directory
)
from werkzeug.utils import secure_filename

from flask_login import current_user, login_required, fresh_login_required

from . import user
from .forms import (
	EditProfile_form, ChangeEmail_form, ChangeLogin_form, 
	ChangePassword_form, EditNotice_form, AddNotice_form
)
from ..models.user import User
from ..models.post import Post
from ..models.notice import Notice
from ..models.comment import Comment
from ..models.user_settings import UserSettings
from ..email import send_email
from ..utils import create_response
from .. import db

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@user.route(rule='/<username>')
def profile_page(username):
	'''Генерирует страницу профиля пользователя.'''
	user = User.query.filter_by(name=username).first_or_404()
	
	if current_user.name == username:
		posts = user.posts.filter(Post.state!='moderator')
		comments = user.comments.filter(Comment.state!='moderation')
	else:
		posts = user.posts.filter_by(state='public')
		comments = user.comments.filter_by(state='public')
	
	return create_response(template='user/profile.html', data={
		'page_title': 'Страница профиля',
		'page': 'profile',
		'user': user,
		'posts': posts,
		'comments': comments
	})



@user.route(rule='/<username>/settings/profile', methods=['GET', 'POST'])
@login_required
def editProfile_page(username):
	'''Генерирует страницу настроек пользователя'''
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
				photo_base_url = os.path.join(upload_folder, 'photos', filename)
				photo.save(photo_base_url)

				user.photo_url = 'photos/' + filename
			else:
				flash(category='warn', 
					message='Поддерживаются только следующие форматы: png, jpg, jpeg, gif, svg')
				return redirect(url_for('user.editProfile_page'))

		user.first_name = first_name
		user.last_name = last_name
		user.about_me = about
		user.location = location

		db.session.add(user)
		db.session.commit()
		
		flash(message='Новые данные сохранены.', category='success')
		return redirect(url_for('user.editProfile_page'))
	
	return create_response(template='user/edit_profile.html', data={
		'page_title': 'Страница редактирования профиля',
		'page': 'edit_profile',
		'form': form
	})



@user.route(rule='/<username>/settings/account')
@login_required
def editAccount_page(username):
	changeLogin_form = ChangeLogin_form()
	changePassword_form = ChangePassword_form()
	changeEmail_form = ChangeEmail_form()

	return create_response(template='user/edit_account.html', data={
		'page_title': 'Страница редактирования аккаунта',
		'page': 'edit_account',
		'login_form': changeLogin_form,
		'password_form': changePassword_form,
		'email_form': changeEmail_form
	})



@user.route(rule='/change_login', methods=['POST'])
@login_required
def changeLogin_request():
	form = ChangeLogin_form()

	if form.validate_on_submit():
		name = form.name.data
		if not User.query.filter_by(name=name).first():
			current_user.name = name
			flash(category='success', message='Ваш login успешно изменён.')
			db.session.add(current_user)
			db.session.commit()
			return redirect(url_for('user.editAccount_page'))
		else:
			flash(category='warn', message='Логин: {} - уже занят'.format(name))
			return redirect(url_for('user.editAccount_page'))
	else:
		flash(category='error', message='Неверные данные')
		return redirect(url_for('user.editAccount_page'))




@user.route(rule='/change_password', methods=['POST'])
@login_required
def changePassword_request():
	form = ChangePassword_form()

	if form.validate_on_submit():
		if current_user.verify_password(form.old_password.data):
			current_user.password = form.password.data

			flash(category='success', message='Ваш пароль успешно изменён.')
			db.session.add(current_user)
			db.session.commit()
			return redirect(url_for('user.editAccount_page'))
		else:
			flash(category='error', message='Неверный пароль.')
			return redirect(url_for('user.editAccount_page'))
	else:
		flash(category='error', message='Неверно заполнена форма.')
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
		flash(message='''На ваш новый почтовый адрес отправленно письмо с инструкциями,
				для потверждения нового адреса''')
		return redirect(url_for('user.editAccount_page'))
	else:
		flash(category='error', message='Неверно заполнена форма.')
		return redirect(url_for('user.editAccount_page'))



@user.route(rule='/change_email/<token>')
@login_required
def changeEmail(token):
	'''Обрабатывает запрос на изменения email.'''
	if current_user.change_email(token):
		db.session.commit()
		flash(category='success', message='Ваш email адрес обновлён.')
		return redirect(url_for('user.editAccount_page'))
	else:
		flash(category='error', message='Неверный запрос.')
		return redirect(url_for('user.editAccount_page'))
	


@user.route(rule='/follow/<user_id>')
@login_required
def follow(user_id):
	user = User.query.filter_by(id=user_id).first()
	if user is None:
		flash(category='error', message='Недействительный пользователь.')
		return redirect(url_for('main.home_page'))
	if current_user.is_following(user):
		flash(category='warn', message='Вы уже читаете данного пользователя.')
		return redirect(url_for('user.profile_page', username=user.name))
	
	current_user.follow(user)
	user_settings = UserSettings.query.filter_by(state='custom', profile=user).first()
	if user_settings.follow_me:
		notice_title = 'На вас подписались'
		notice_body = '<a href="{}">{}</a> - подписался на вас.'.format(
			url_for('user.profile_page', username=current_user.name), current_user.name
		)
		notice = Notice(title=notice_title, body=notice_body, author=user)

		db.session.add(notice)
		db.session.commit()
	flash(category='success', message='Вы подписаны на {}'.format(user.name))
	return redirect(url_for('user.profile_page', username=user.name))



@user.route(rule='/unfollow/<user_id>')
@login_required
def unfollow(user_id):
	'''Реализовывает отписку от пользователя'''
	user = User.query.filter_by(id=user_id).first()
	if not current_user.is_following(user):
		flash(category='warn', message='Вы уже отписаны.')
		return redirect(url_for('user.profile_page', username=user.name))
	current_user.unfollow(user)

	user_settings = UserSettings.query.filter_by(state='custom', profile=user).first()
	if user_settings.unfollow_me:
		notice_title = 'От вас отписались'
		notice_body = '<a href="{}">{}</a> - отписался от вас.'.format(
			url_for('user.profile_page', username=current_user.name), current_user.name
		)
		notice = Notice(title=notice_title, body=notice_body, author=user)

		db.session.add(notice)
		db.session.commit()

	flash(category='success', message='Вы отписаны от {}'.format(user.name))
	return redirect(request.cookies.get('current_page'))


@user.route(rule='/unsubscribe/<user_id>')
@login_required
def unsubscribe(user_id):
	'''Реализовывает возможность текущему пользователю отписывать тех
	кто на него подписан'''
	user = User.query.filter_by(id=user_id).first()
	user.unfollow(current_user)

	user_settings = UserSettings.query.filter_by(state='custom', profile=user).first()
	if user_settings.unsubscribe_me:
		notice_title = 'Вас удалили из подписчиков'
		notice_body = '<a href="{}">{}</a> - удалил вас из подписчиков.'.format(
			url_for('user.profile_page', username=current_user.name), current_user.name
		)
		notice = Notice(title=notice_title, body=notice_body, author=user)

		db.session.add(notice)
		db.session.commit()

	flash(category='success', message='Вы удалили {} из ваших подписчиков'.format(user.name))
	return redirect(request.cookies.get('current_page'))



@user.route(rule='/<username>/followers/')
def followers_page(username):
	user = User.query.filter_by(name=username).first()

	if user is None:
		abort(404)
		return redirect(url_for('main.home_page'))
	
	count_items = current_app.config['APP_FOLLOWERS_PER_PAGE']

	if current_user == user:
		posts = user.posts.filter(Post.state!='moderator')
		comments = user.comments.filter(Comment.state!='moderation')
	else:
		posts = user.posts.filter_by(state='public')
		comments = user.comments.filter_by(state='public')
	
	page = request.args.get('page', 1, type=int)
	pagination = user.followers.paginate(
		page, per_page=count_items, error_out=False)
	follows = [{'user': item.follower, 'timestamp': item.timestamp} 
				for item in pagination.items] 

	return create_response(template='user/followers.html', data={
		'page_title': 'Страница подписчиков.',
		'page': 'followers',
		'user': user,
		'posts': posts,
		'comments': comments,
		'pagination': pagination,
		'follows': follows,
		'follows_count': len(follows),
		'endpoint': 'user.followers_page',
		'title': 'Подписчики',
		'unfollow_btn': False,
		'count_items': count_items
	})



@user.route(rule='/<username>/followed_by/')
def followedBy_page(username):
	'''Генерирует страницу пользователей на которых подписан 
	указанный пользователь'''
	user = User.query.filter_by(name=username).first()

	if user is None:
		abort(404)
		return redirect(url_for('main.home_page'))
	
	count_items = current_app.config['APP_FOLLOWERS_PER_PAGE']

	if current_user == user:
		posts = user.posts.filter(Post.state!='moderator')
		comments = user.comments.filter(Comment.state!='moderation')
	else:
		posts = user.posts.filter_by(state='public')
		comments = user.comments.filter_by(state='public')

	page = request.args.get('page', 1, type=int)
	pagination = user.followed.paginate(
		page, per_page=count_items, error_out=False)
	follows = [{'user': item.followed, 'timestamp': item.timestamp} 
				for item in pagination.items]

	return create_response(template='user/followers.html', data={
		'page_title': 'Страница подписок.',
		'page': 'followed',
		'user': user,
		'posts': posts,
		'comments': comments,
		'pagination': pagination,
		'follows': follows,
		'follows_count': len(follows),
		'endpoint': 'user.followedBy_page',
		'title': 'Подписан.',
		'unfollow_url': 'user.unfollow',
		'unfollow_btn': True,
		'count_items': count_items
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


@user.route('/<username>/settings/notice')
@login_required
def editNotice_page(username):
	form = EditNotice_form()
	user_settings = UserSettings.query.filter_by(state='custom', profile=current_user).first()

	form.comments_me.data = user_settings.comments_me
	form.follow_me.data = user_settings.follow_me
	form.unfollow_me.data = user_settings.unfollow_me
	form.unsubscribe_me.data = user_settings.unsubscribe_me
	form.comment_moderated.data = user_settings.comment_moderated
	form.post_moderated.data = user_settings.post_moderated

	return create_response(template='user/edit_notice.html', data={
		'page_title': 'Страница настроек уведомлений',
		'page': 'edit_notice',
		'form': form
	})


@user.route('/<username>/admin/')
@login_required
def adminDashboard_page(username):
	comments = []
	for i in current_user.posts:
		com = i.comments.filter_by(state='moderation')
		comments.extend(com)

	user = User.query.filter_by(name=username).first()

	return create_response(template='user/admin/dashboard.html', data={
		'title_page': 'Страница администрирования',
		'page': 'dashboard',
		'comments': comments,
		'user': user
	})


@user.route('/<username>/admin/comments/')
@login_required
def adminComments_page(username):
	comments = []
	for i in current_user.posts:
		com = i.comments.filter_by(state='moderation')
		comments.extend(com)
	
	posts = Post.query.filter_by(state='moderation')
	
	return create_response(template='user/admin/comments.html', data={
		'title_page': 'Страница модерации комментариев',
		'page': 'comments',
		'comments': comments,
		'posts': posts
	})


@user.route('/<username>/admin/coments/<int:id>')
@login_required
def adminComment_page(username, id):
	posts = Post.query.filter_by(state='moderation')
	comment = Comment.query.get_or_404(id)
	comments = []
	for i in current_user.posts:
		com = i.comments.filter_by(state='moderation')
		comments.extend(com)
	
	if comment.state == 'public':
		state_body = 'Опубликован'
	if comment.state == 'develop':
		state_body = 'Находится на доработке'
	if comment.state != 'moderation':
		return create_response(template='state.html', data={
			'title_page': 'Стадия контента',
			'state_title': 'Комментарий',
			'posts': Post.query.filter_by(state='public'),
			'followed_posts': current_user.followed_posts.filter(Post.state=='public'),
			'state_body': state_body
		})
	else:
		return create_response(template='user/admin/comment.html', data={
			'title_page': 'Страница модерации комментария',
			'comment': comment,
			'comments': comments,
			'posts': posts
		})


@user.route('/<username>/admin/comments/<int:id>/...return')
@login_required
def adminReturnComment_page(username, id):
	form = AddNotice_form()
	comment = Comment.query.get_or_404(id)
	posts = Post.query.filter_by(state='moderation')
	comments = []
	for i in current_user.posts:
		com = i.comments.filter_by(state='moderation')
		comments.extend(com)

	return create_response(template='user/admin/noticeComment_form.html', data={
		'title_page': 'Страница формы уведомления',
		'form': form,
		'comment': comment,
		'posts': posts,
		'comments': comments
	})