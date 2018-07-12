# moderator/views.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from functools import wraps

from flask import redirect, request, url_for, flash

from flask_login import current_user, login_required

from . import moderator
from .forms import AddNotice_form
from .utils import is_moderator
from ..models.post import Post
from ..utils import create_response

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@moderator.route('/')
@is_moderator
def dashboard_page():
    '''Генерирует панель модератора.'''
    posts = Post.query.filter_by(state='moderation')

    return create_response('moderator/dashboard.html', data={
        'title_page': 'Страница модератора.',
        'posts': posts,
        'page': 'dashboard'
    })


@moderator.route('/posts')
@is_moderator
def posts_page():
    '''Генерирует страницу публикаций для модерации.'''
    posts = Post.query.filter_by(state='moderation')

    return create_response('moderator/posts.html', data={
        'title_page': 'Страница публикации для модерации',
        'posts': posts,
        'page': 'posts'
    })


@moderator.route('/posts/<int:id>')
@is_moderator
def post_page(id):
    post = Post.query.get_or_404(id)
    posts = Post.query.filter_by(state='moderation')
    tags = post.tags.all()

    return create_response(template='moderator/post.html', data={
        'title_page': 'Страница публикации',
        'posts': posts,
        'post': post,
        'tags': tags
    })


@moderator.route('/posts/<int:id>...return')
@is_moderator
def returnPost_page(id):
    form = AddNotice_form()
    post = Post.query.get(id)
    posts = Post.query.filter_by(state='moderation')

    return create_response(template='moderator/notice_form.html', data={
        'title_page': 'Страница формы уведомления',
        'form': form,
        'post': post,
        'posts': posts
    })

