# main/views.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import (
    render_template, request, current_app, make_response, redirect, 
    url_for, current_app, flash
)

from flask_login import current_user, login_required
from flask_sqlalchemy import get_debug_queries

from . import main
from .forms import Search_form
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
    return create_response(template='index.html', data={
        'page_title': 'Главная страница.',
        'tags': Tag.query.all(),
        'form': Search_form()
    })



@main.route('/posts/search_results/<data>')
def searchResults_page(data):
    '''Генерирует страницу с результатами поиска.'''
    if current_user.is_anonymous:
        followed_posts = None
    else:
        followed_posts = current_user.followed_posts.filter(Post.state=='public')
    
    count_items = current_app.config['APP_POSTS_PER_PAGE']
    page = request.args.get('page', 1, type=int)

    posts, total = Post.search(data, page, count_items)

    next_url = url_for('main.search_request', q=data, page=page + 1) \
        if total > page * count_items else None
    prev_url = url_for('main.search_request', q=data, page=page - 1) \
        if page > 1 else None

    flash(category='success', 
        message='Показаны результаты по запросу: <br><b>{}</b>'.format(data))

    return create_response(template='post/search_results.html', data={
        'page_title': 'Search results',
        'page_posts': posts,
        'all_posts': Post.query.filter_by(state='public'),
        'followed_posts': followed_posts,
        'total': total,
        'next_url': next_url,
        'prev_url': prev_url,
        'current_page': page
    })

