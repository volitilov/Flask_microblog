# post/routes/pages.py

# Обрабатывает GET-запросы
# Формирует страницы для запрошенных урлов 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

import urllib
from flask import request, flash, current_app, redirect, url_for, abort
from flask_login import current_user, login_required

from .. import (
    # blueprint
    post,

    # utils
    create_response,

    # models
    Post, User, Comment, Post_rating, Tag,

    # forms
    AddPost_form, EditPost_form,

    # database
    db,

    # data
    get_posts, page_titles
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@post.route(rule='/posts/<int:id>/...edit')
@login_required
def editPost_page(id):
    '''Генерирует страницу редактирования поста.'''
    data = get_posts()
    form = EditPost_form()
    post = Post.query.get_or_404(id)

    if current_user != post.author:
        abort(403)
    
    if post.state == 'moderation':
        return redirect(url_for('post.post_page', id=post.id))
    
    form.text.data = post.text
    form.contents.data = post.table_of_contents

    tags = []
    for rel_tag in post.tags.all():
        tags.append(rel_tag.tag.name)
    form.tags.data = ', '.join(tags)

    return create_response(template='post/edit_post.html', data={
        'page_title': page_titles['editPost_page'],
        'form': form,
        'post': post,
        'all_posts': data['all_posts'],
        'followed_posts': data['followed_posts']
    })



@post.route(rule='/posts/...add')
@login_required
def addPost_page():
    '''Генерирует страницу с формай создания постов.'''
    if not current_user.writer:
        flash(message='Вы не можете писать посты пока не станите автором.')
        return redirect('/posts/63')
    data = get_posts()
    form = AddPost_form()
    return create_response(template='post/add_post.html', data={
        'page_title': page_titles['addPost_page'],
        'form': form,
        'all_posts': data['all_posts'],
        'followed_posts': data['followed_posts']
    })



@post.route('/posts/')
def posts_page():
    '''Генерирует страницу со всеми публикациями.'''
    data = get_posts()
    count_items = current_app.config['APP_POSTS_PER_PAGE']
    posts = data['all_posts'].order_by(Post.data_creation.desc())
    page = request.args.get('page', 1, type=int)
    pagination = posts.paginate(
        page, per_page=count_items, error_out=False)

    return create_response(template='post/posts.html', data={
        'page_title': page_titles['posts_page'],
        'pagination': pagination,
        'all_posts': posts,
        'page_posts': pagination.items,
        'endpoint': 'post.posts_page',
        'page': 'all_posts',
        'followed_posts': data['followed_posts'],
        'count_items': count_items
    })



@post.route('/posts/followed_posts/')
@login_required
def followedPosts_page():
    '''Создаёт страницу с побликациями пользователей на которых подписан
    текущий пользователь'''
    data = get_posts()
    count_items = current_app.config['APP_POSTS_PER_PAGE']

    page = request.args.get('page', 1, type=int)
    pagination = data['followed_posts'].order_by(Post.data_creation.desc()).paginate(
        page, per_page=count_items, error_out=False)

    return create_response(template='post/posts.html', data={
        'page_title': page_titles['followedPosts_page'],
        'pagination': pagination,
        'page_posts': pagination.items,
        'all_posts': data['all_posts'],
        'page': 'followed_posts',
        'endpoint': 'post.followedPosts_page',
        'followed_posts': data['followed_posts'],
        'count_items': count_items
    })



@post.route(rule='/posts/<username>/posts/')
def userPosts_page(username):
    '''Генерирует страницу с публикациями пользователя.'''
    user = User.query.filter_by(name=username).first()
    count_items = current_app.config['APP_POSTS_PER_PAGE']
    posts = user.posts.filter_by(state='public')
    comments = user.comments.filter_by(state='public')

    if not current_user.is_anonymous:
        if current_user.name == username:
            posts = user.posts.filter(Post.state!='moderation')
            comments = user.comments.filter(Comment.state!='moderation')

    page = request.args.get('page', 1, type=int)
    pagination = posts.order_by(Post.data_creation.desc()).paginate(
        page, per_page=count_items, error_out=False)

    return create_response(template='post/user_posts.html', data={
        'page_title': page_titles['userPosts_page'],
        'page': 'user_posts',
        'page_posts': pagination.items,
        'pagination': pagination,
        'endpoint': 'post.userPosts_page',
        'user': user,
        'posts': posts,
        'comments': comments,
        'posts_per_page': count_items
    })



@post.route(rule='/posts/tag/<int:id>/')
def tagPosts_page(id):
    '''Генерирует страницу с публикациями по запрошенному тегу.'''
    data = get_posts()
    tag = Tag.query.get_or_404(id)
    posts = tag.posts
    count_items = current_app.config['APP_POSTS_PER_PAGE']

    page = request.args.get('page', 1, type=int)

    pagination = posts.paginate(
        page, per_page=count_items, error_out=False)
    tag_posts = [{
        'id': item.post.id,
        'title': item.post.title, 
        'data_creation': item.post.data_creation, 
        'author': item.post.author,
        'views': item.post.views,
        'rating': item.post.rating,
        't_contents_html': item.post.t_contents_html
        } for item in pagination.items if item.post.state=='public']

    flash(category='success', 
        message='Показаны результаты запроса по тегу <b>{}</b>'.format(tag.name))

    print(data['all_posts'].count() > count_items)

    return create_response(template='post/posts.html', data={
        'page_title': page_titles['tagPosts_page'],
        'page_posts': tag_posts,
        'pagination': pagination,
        'endpoint': 'post.tagPosts_page',
        'tag': tag,
        'count_items': count_items,
        'all_posts': data['all_posts'],
        'followed_posts': data['followed_posts']
    })



@post.route(rule='/posts/<int:id>')
def post_page(id):
    '''Генерирует страницу запрошенного поста'''
    data = get_posts()
    post = Post.query.get_or_404(id)
    tags = post.tags
    
    if current_user != post.author:
        post.views += 1
        db.session.add(post)
        db.session.commit()

    rating_bool = False
    
    if current_user.is_anonymous:
        rating_bool = False
    else:
        if Post_rating.query.filter_by(post=post, author=current_user).first():
            rating_bool = True

        if post.author == current_user:
            rating_bool = True

    if post.state == 'public' or post.state == 'develop' \
        and post.author == current_user:
        return create_response(template='post/post.html', data={
            'page_title': post.title,
            'post': post,
            'comments': post.comments.filter(Comment.state=='public'),
            'rating_bool': rating_bool,
            'tags': tags,
            'all_posts': data['all_posts'],
            'followed_posts': data['followed_posts'],
            'base_url': request.base_url
        })
    if post.state == 'moderation':
        state_body = 'Находится на модерации'
    if post.state == 'develop':
        state_body = 'Находится на доработке'
    if post.state != 'public':
        return create_response(template='post/state.html', data={
            'page_title': 'Стадия контента',
            'state_title': 'Пост',
            'state_body': state_body,
            'all_posts': data['all_posts'],
            'followed_posts': data['followed_posts']
        })



@post.route(rule='/posts/by_viewing/')
def byViewingPosts_page():
    '''Формирует страницу постов отсортированных по кол-ву просмотров.'''
    data = get_posts()
    count_items = current_app.config['APP_POSTS_PER_PAGE']

    page = request.args.get('page', 1, type=int)
    posts = data['all_posts'].order_by(Post.views.desc())
    pagination = posts.paginate(page, 
        per_page=count_items, error_out=False)

    return create_response(template='post/posts.html', data={
        'page_title': page_titles['byViewingPosts_page'],
        'page': 'post_views',
        'page_posts': pagination.items,
        'all_posts': data['all_posts'],
        'pagination': pagination,
        'endpoint': 'post.byViewingPosts_page',
        'followed_posts': data['followed_posts'],
        'count_items': count_items
    })



@post.route(rule='/posts/by_rating/')
def byRatingPosts_page():
    '''Формирует страницу постов отсортированных по рейтингу.'''
    data = get_posts()
    count_items = current_app.config['APP_POSTS_PER_PAGE']

    page = request.args.get('page', 1, type=int)
    posts = data['all_posts'].order_by(Post.rating.desc())
    pagination = posts.paginate(page, 
        per_page=count_items, error_out=False)

    return create_response(template='post/posts.html', data={
        'page_title': page_titles['byRatingPosts_page'],
        'page': 'post_ratings',
        'page_posts': pagination.items,
        'all_posts': data['all_posts'],
        'pagination': pagination,
        'endpoint': 'post.byRatingPosts_page',
        'followed_posts': data['followed_posts'],
        'count_items': count_items
    })