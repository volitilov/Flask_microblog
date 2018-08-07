# comment/routes/page.py

# Обрабатывает GET-запросы
# Формирует страницы для запрошенных урлов 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import redirect, request, url_for, flash

from flask_login import current_user, login_required

from .. import (
	# blueprint
	comment,

	# utils
	create_response,

	# forms
	AddComment_form,

	# data 
	page_titles, get_data,
	
	# models 
	Post, User, Comment,

	# database
	db
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@comment.route(rule='/<username>/comments/')
def comments_page(username):
	'''Генерирует страницу с комментариями пользователя.'''
	user = User.query.filter_by(name=username).first()
	data = get_data(current_user, user)

	comments = data['comments'].order_by(Comment.timestamp.desc())

	return create_response(template='comments.html', data={
		'page_title': page_titles['comments_page'],
		'page': 'comments',
		'comments': comments,
		'posts': data['posts'],
		'user': user
	})


@comment.route(rule='/comments/<int:id>')
def comment_page(id):
	'''Генерирует страница для запрошенного комментария.'''
	comment = Comment.query.get_or_404(id)
	user = comment.author
	data = get_data(current_user, user)

	if comment.state == 'public' or \
		comment.state == 'develop' and user == current_user:
			return create_response(template='comment.html', data={
				'page_title': page_titles['comment_page'],
				'comment': comment,
				'posts': data['posts'],
				'comments': data['comments'],
				'user': comment.author
			})
	else:
		if comment.state == 'moderation':
			state_body = 'Находится на модерации'
		if comment.state == 'develop':
			state_body = 'Находится на доработке'
		if comment.state != 'public':
			return create_response(template='state.html', data={
				'page_title': 'Стадия контента',
				'state_title': 'Комментарий',
				'posts': data['posts'],
				'followed_posts': current_user.followed_posts.filter(Post.state=='public'),
				'state_body': state_body
			})

