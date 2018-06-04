# main/views.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import (
	render_template, request, current_app, make_response, redirect, 
	url_for
)

from flask_login import current_user, login_required
from flask_sqlalchemy import get_debug_queries

from . import main
from ..models.post import Post
from ..utils import create_response

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@main.after_app_request
def after_request(response):
	'''Ведёт отчёт в виде списка о медлиных запросов к базе данных'''
	for query in get_debug_queries():
		if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
			current_app.logger.warning(
				'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
				% (query.statement, query.parameters, query.duration,
				query.context))
	return response


@main.route('/')
def home_page():
	'''Генерирует стартовую страницу.'''
	count_items = current_app.config['FLASKY_POSTS_PER_PAGE']

	if not current_user.is_anonymous:
		show_followed = bool(request.cookies.get(key='show_followed'))
	else:
		show_followed = False
	if show_followed:
		query = current_user.followed_posts
		print(current_user.followed_posts)
	else:
		query = Post.query
	
	page = request.args.get('page', 1, type=int)
	pagination = query.order_by(Post.data_creation.desc()).paginate(
		page, per_page=count_items, error_out=False)

	return create_response(template='index.html', data={
		'page_title': 'Главная страница.',
		'posts': pagination.items,
		'pagination': pagination,
		'posts': pagination.items,
		'show_followed': show_followed
	})


@main.route('/all_posts')
@login_required
def allPosts_request():
	resp = make_response(redirect(url_for('main.home_page')))
	resp.set_cookie(key='show_followed', value='', max_age=30*24*60*60)
	return resp



@main.route('/followed_posts')
@login_required
def followedPosts_request():
	resp = make_response(redirect(url_for('main.home_page')))
	resp.set_cookie(key='show_followed', value='1', max_age=30*24*60*60)
	return resp