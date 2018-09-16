# main/routes/pages.py

# Обрабатывает GET-запросы
# Формирует страницы для запрошенных урлов 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import request, current_app, url_for, current_app, flash
from flask_login import current_user, login_required

from .. import (
    # blueprint
    main,

    # forms
    Search_form, Support_form,

    # models
    Post, Tag,

    # utils
    create_response,

    # data
    page_titles
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@main.route('/')
def home_page():
    '''Генерирует стартовую страницу.'''
    return create_response(template='main/home.html', data={
        'page_title': page_titles['home_page'],
        'tags': Tag.query.all()[:5],
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
    posts = posts.filter_by(state='public')

    count_page = total // count_items
    if total - (count_page * count_items):
        count_page += 1

    next_url = url_for('main.searchResults_page', data=data, page=page + 1) \
        if total > page * count_items else None
    prev_url = url_for('main.searchResults_page', data=data, page=page - 1) \
        if page > 1 else None

    flash(category='success', 
        message='Показаны результаты по запросу: <br><b>{}</b>'.format(data))

    return create_response(template='main/search_results.html', data={
        'page_title': page_titles['searchResults_page'],
        'page_posts': posts,
        'all_posts': Post.query.filter_by(state='public'),
        'followed_posts': followed_posts,
        'total': total,
        'next_url': next_url,
        'prev_url': prev_url,
        'count_page': range(count_page),
        'data': data,
        'current_page': page
    })



@main.route('/all_tags')
def allTags_page():
    '''Генерирует страницу всех тегов.'''
    if current_user.is_anonymous:
        followed_posts = None
    else:
        followed_posts = current_user.followed_posts.filter(Post.state=='public')

    return create_response(template='main/all_tags.html', data={
        'page_title': page_titles['allTags_page'],
        'tags': Tag.query.all(),
        'all_posts': Post.query.filter_by(state='public'),
        'followed_posts': followed_posts,
    })



@main.route('/support')
@login_required
def support_page():
    '''Генерирует страницу с формой службы поддержки'''
    form = Support_form()

    if current_user.is_anonymous:
        followed_posts = None
    else:
        followed_posts = current_user.followed_posts.filter(Post.state=='public')

    return create_response(template='main/support.html', data={
        'page_title': page_titles['support_page'],
        'form': form,
        'all_posts': Post.query.filter_by(state='public'),
        'followed_posts': followed_posts,
    })