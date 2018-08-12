# user/routes/pages.py

# Обрабатывает GET-запросы
# Формирует страницы для запрошенных урлов 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import (
    redirect, request, url_for, flash, session, abort, current_app
)
from flask_login import current_user, login_required

from .. import (
    # blueprint
    user,

    # models
    User, Post, Comment,

    # utils
    create_response,

    # database
    db
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@user.route(rule='/<username>')
def profile_page(username):
    '''Генерирует страницу профиля пользователя.'''
    user = User.query.filter_by(name=username).first_or_404()
    posts = user.posts.filter_by(state='public')
    comments = user.comments.filter_by(state='public')
    
    if not current_user.is_anonymous:
        if current_user.name == username:
            posts = user.posts.filter(Post.state!='moderator')
            comments = user.comments.filter(Comment.state!='moderation')
    
    return create_response(template='profile.html', data={
        'page_title': 'Страница профиля',
        'page': 'profile',
        'user': user,
        'posts': posts,
        'comments': comments
    })



@user.route(rule='/<username>/settings/account')
@login_required
def editAccount_page(username):
    return create_response(template='edit_account.html', data={
        'page_title': 'Страница редактирования аккаунта',
        'page': 'edit_account'
    })



@user.route(rule='/<username>/followers/')
def followers_page(username):
    user = User.query.filter_by(name=username).first()
    posts = user.posts.filter_by(state='public')
    comments = user.comments.filter_by(state='public')

    if user is None:
        abort(404)
        return redirect(url_for('main.home_page'))
    
    count_items = current_app.config['APP_FOLLOWERS_PER_PAGE']

    if not current_user.is_anonymous:
        if current_user == user:
            posts = user.posts.filter(Post.state!='moderator')
            comments = user.comments.filter(Comment.state!='moderation')
    
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=count_items, error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp} 
                for item in pagination.items] 

    return create_response(template='followers.html', data={
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
    posts = user.posts.filter_by(state='public')
    comments = user.comments.filter_by(state='public')

    if user is None:
        abort(404)
        return redirect(url_for('main.home_page'))
    
    count_items = current_app.config['APP_FOLLOWERS_PER_PAGE']

    if not current_user.is_anonymous:
        if current_user == user:
            posts = user.posts.filter(Post.state!='moderator')
            comments = user.comments.filter(Comment.state!='moderation')

    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=count_items, error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp} 
                for item in pagination.items]

    return create_response(template='followers.html', data={
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



@user.route('/<username>/admin/')
@login_required
def adminDashboard_page(username):
    comments = []
    for i in current_user.posts:
        com = i.comments.filter_by(state='moderation')
        comments.extend(com)

    user = User.query.filter_by(name=username).first()

    return create_response(template='admin/dashboard.html', data={
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
    
    return create_response(template='admin/comments.html', data={
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
        return create_response(template='admin/comment.html', data={
            'title_page': 'Страница модерации комментария',
            'comment': comment,
            'comments': comments,
            'posts': posts
        })

