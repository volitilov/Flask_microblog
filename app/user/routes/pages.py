# user/routes/pages.py

# Обрабатывает GET-запросы
# Формирует страницы для запрошенных урлов 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import (
    redirect, request, url_for, flash, session, abort, current_app, abort
)
from flask_login import current_user, login_required, fresh_login_required

from .. import (
    # blueprint
    user,

    # models
    User, Post, Comment,

    # forms
    EditProfile_form, ChangeLogin_form, ChangePassword_form,
    ChangeEmail_form, AddNotice_form,

    # utils
    create_response,

    # database
    db,

    # data
    page_titles
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@user.route('/<username>/admin/comments/<int:id>/...return')
@login_required
def adminReturnComment_page(username, id):
    '''Генерирует и обрабатывает страницу возврата комментария на доработку'''
    form = AddNotice_form()
    comment = Comment.query.get_or_404(id)
    posts = Post.query.filter_by(state='moderation')
    comments = []

    if username != current_user.name:
        abort(403)
    
    for i in current_user.posts:
        com = i.comments.filter_by(state='moderation')
        comments.extend(com)

    return create_response(template='user/admin/noticeComment_form.html', data={
        'title_page': page_titles['adminReturnComment_page'],
        'form': form,
        'comment': comment,
        'posts': posts,
        'comments': comments
    })



@user.route(rule='/settings/account/change_email')
@fresh_login_required
def changeEmail_page():
    '''Генерирует и обрабатывает страницу изменения email'''
    form = ChangeEmail_form()
    form.email.data = current_user.email

    return create_response(template='user/change_email.html', data={
        'page_title': page_titles['changeEmail_page'],
        'form': form
    })



@user.route(rule='/settings/account/change_password')
@fresh_login_required
def changePassword_page():
    '''Генерирует и обрабатывает страницу изменения пароля'''
    form = ChangePassword_form()

    return create_response(template='user/change_password.html', data={
        'page_title': page_titles['changePassword_page'],
        'form': form
    })



@user.route(rule='/settings/accout/change_login')
@fresh_login_required
def changeLogin_page():
    '''Генерирует и обрабатывает страницу изменения логина'''
    form = ChangeLogin_form()
    form.name.data = current_user.name

    return create_response(template='user/change_login.html', data={
        'page_title': page_titles['changeLogin_page'],
        'form': form
    })



@user.route(rule='/settings/profile')
@login_required
def editProfile_page():
    '''Генерирует и обрабатывает страницу настроек пользователя'''
    form = EditProfile_form()
    
    form.first_name.data = current_user.first_name
    form.last_name.data = current_user.last_name
    form.about.data = current_user.about_me
    form.location.data = current_user.location
    
    return create_response(template='user/edit_profile.html', data={
        'page_title': page_titles['editProfile_page'],
        'page': 'edit_profile',
        'form': form
    })



@user.route(rule='/profile/<username>')
def profile_page(username):
    '''Генерирует страницу профиля пользователя.'''
    user = User.query.filter_by(name=username).first_or_404()
    posts = user.posts.filter_by(state='public')
    comments = user.comments.filter_by(state='public')
    
    if not current_user.is_anonymous and \
        current_user.name == username:
            posts = user.posts.filter(Post.state!='moderation')
            comments = user.comments.filter(Comment.state!='moderation')
    
    return create_response(template='user/profile.html', data={
        'page_title': page_titles['profile_page'],
        'page': 'profile',
        'user': user,
        'posts': posts,
        'comments': comments
    })



@user.route(rule='/settings/account')
@login_required
def editAccount_page():
    '''Генерирует страницу редактирования аккаунта.'''
    return create_response(template='user/edit_account.html', data={
        'page_title': page_titles['editAccount_page'],
        'page': 'edit_account'
    })



@user.route(rule='/<username>/followers/')
def followers_page(username):
    '''Генерирует страницу подписчиков.'''
    user = User.query.filter_by(name=username).first()
    posts = user.posts.filter_by(state='public')
    comments = user.comments.filter_by(state='public')

    if user is None:
        abort(404)
        return redirect(url_for('main.home_page'))
    
    count_items = current_app.config['APP_FOLLOWERS_PER_PAGE']

    if not current_user.is_anonymous:
        if current_user == user:
            posts = user.posts.filter(Post.state!='moderation')
            comments = user.comments.filter(Comment.state!='moderation')
    
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=count_items, error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp} 
                for item in pagination.items] 

    return create_response(template='user/followers.html', data={
        'page_title': page_titles['followers_page'],
        'page': 'followers',
        'user': user,
        'posts': posts,
        'comments': comments,
        'pagination': pagination,
        'follows': follows,
        'follows_count': len(follows),
        'endpoint': 'user.followers_page',
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
    
    count_items = current_app.config['APP_FOLLOWERS_PER_PAGE']

    if not current_user.is_anonymous:
        if current_user == user:
            posts = user.posts.filter(Post.state!='moderation')
            comments = user.comments.filter(Comment.state!='moderation')

    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=count_items, error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp} 
                for item in pagination.items]

    return create_response(template='user/followers.html', data={
        'page_title': page_titles['followedBy_page'],
        'page': 'followed',
        'user': user,
        'posts': posts,
        'comments': comments,
        'pagination': pagination,
        'follows': follows,
        'follows_count': len(follows),
        'endpoint': 'user.followedBy_page',
        'unfollow_url': 'user.unfollow',
        'unfollow_btn': True,
        'count_items': count_items
    })



@user.route('/<username>/admin/')
@login_required
def adminDashboard_page(username):
    '''Генерирует главную страницу администрирования пользователя'''
    if username != current_user.name:
        abort(403)

    comments = []
    for i in current_user.posts:
        com = i.comments.filter_by(state='moderation')
        comments.extend(com)

    user = User.query.filter_by(name=username).first()

    return create_response(template='user/admin/dashboard.html', data={
        'title_page': page_titles['adminDashboard_page'],
        'page': 'dashboard',
        'comments': comments,
        'user': user
    })



@user.route('/<username>/admin/comments/')
@login_required
def adminComments_page(username):
    '''Генерирует страницу администрирования комментариев к постам текущего
    пользователя'''
    if username != current_user.name:
        abort(403)

    comments = []
    for i in current_user.posts:
        com = i.comments.filter_by(state='moderation')
        comments.extend(com)
    
    posts = Post.query.filter_by(state='moderation')
    
    return create_response(template='user/admin/comments.html', data={
        'title_page': page_titles['adminComments_page'],
        'page': 'comments',
        'comments': comments,
        'posts': posts
    })



@user.route('/<username>/admin/coments/<int:id>')
@login_required
def adminComment_page(username, id):
    '''Генерирует страницу модерирования комментария к посту текущего
    пользователя'''
    if username != current_user.name:
        abort(403)
    
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
            'title_page': page_titles['adminComment_page'],
            'comment': comment,
            'comments': comments,
            'posts': posts
        })

