# main/views.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import (
	render_template, request, current_app, make_response, redirect, 
	url_for, current_app
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
	count_items = current_app.config['APP_POSTS_PER_PAGE']
	posts = Post.query.order_by(Post.data_creation.desc())
	
	page = request.args.get('page', 1, type=int)
	pagination = posts.paginate(
		page, per_page=count_items, error_out=False)

	return create_response(template='index.html', data={
		'page_title': 'Главная страница.',
		'pagination': pagination,
		'posts': pagination.items,
		'endpoint': 'main.home_page',
		'page': 'all_posts',
		'posts_count': posts.count(),
		'posts_per_page': count_items
	})
