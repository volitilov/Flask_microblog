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
from ..models.tag import Tag
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
	tags = Tag.query.all()

	return create_response(template='index.html', data={
		'page_title': 'Главная страница.',
		'tags': tags
	})
