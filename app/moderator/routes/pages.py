# moderator/routes/pages.py

# Обрабатывает GET-запросы
# Формирует страницы для запрошенных урлов 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import current_app

from .. import (
    # blueprint
    moderator,

    # forms
    AddNotice_form,

    # utils
    is_moderator, create_response,

    # models
    Post, Message, User,

    # data
    page_titles, get_data
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@moderator.route('/moderator')
@is_moderator
def dashboard_page():
    '''Генерирует панель модератора.'''
    data = get_data()

    return create_response('mod_dashboard.html', data={
        'title_page': page_titles['dashboard_page'],
        'posts': data['posts'],
        'comments': data['comments'],
        'messages': data['messages'],
        'page': 'dashboard'
    })



@moderator.route('/moderator/posts')
@is_moderator
def posts_page():
    '''Генерирует страницу публикаций для модерации.'''
    data = get_data()

    return create_response('mod_posts.html', data={
        'title_page': page_titles['posts_page'],
        'posts': data['posts'],
        'comments': data['comments'],
        'messages': data['messages'],
        'page': 'posts'
    })



@moderator.route('/moderator/posts/<int:id>')
@is_moderator
def post_page(id):
    data = get_data()
    post = Post.query.get_or_404(id)
    tags = post.tags.all()

    return create_response(template='mod_post.html', data={
        'title_page': page_titles['post_page'],
        'posts': data['posts'],
        'post': post,
        'comments': data['comments'],
        'messages': data['messages'],
        'tags': tags
    })



@moderator.route('/moderator/posts/<int:id>...return')
@is_moderator
def returnPost_page(id):
    '''Обрабатывает запросы на отправку уведомлений пользователям о том, 
    что их публикации необходимо доработать.'''
    data = get_data()
    form = AddNotice_form()
    post = Post.query.get_or_404(id)

    return create_response(template='mod_noticePost_form.html', data={
        'title_page': page_titles['returnPost_page'],
        'form': form,
        'post': post,
        'comments': data['comments'],
        'messages': data['messages'],
        'posts': data['posts']
    })



@moderator.route('/moderator/messages/')
def messages_page():
    '''Генерирует страницу сообщений службы поддержки'''
    data = get_data()

    print(data['messages'])

    return create_response(template='mod_messages.html', data={
        'title_page': page_titles['messages_page'],
        'page': 'messages',
        'posts': data['posts'],
        'comments': data['comments'],
        'messages': data['messages']
    })