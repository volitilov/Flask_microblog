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
from ..models.comment import Comment
from ..utils import create_response

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@moderator.route('/')
@is_moderator
def dashboard_page():
    '''Генерирует панель модератора.'''
    comments = Comment.query.filter_by(state='moderation')
    posts = Post.query.filter_by(state='moderation')

    return create_response('moderator/dashboard.html', data={
        'title_page': 'Страница модератора.',
        'posts': posts,
        'comments': comments,
        'page': 'dashboard'
    })


@moderator.route('/posts')
@is_moderator
def posts_page():
    '''Генерирует страницу публикаций для модерации.'''
    posts = Post.query.filter_by(state='moderation')
    comments = Comment.query.filter_by(state='moderation')

    return create_response('moderator/posts.html', data={
        'title_page': 'Страница публикации для модерации',
        'posts': posts,
        'comments': comments,
        'page': 'posts'
    })


@moderator.route('/posts/<int:id>')
@is_moderator
def post_page(id):
    post = Post.query.get_or_404(id)
    posts = Post.query.filter_by(state='moderation')
    comments = Comment.query.filter_by(state='moderation')
    tags = post.tags.all()

    return create_response(template='moderator/post.html', data={
        'title_page': 'Страница публикации',
        'posts': posts,
        'post': post,
        'comments': comments,
        'tags': tags
    })


@moderator.route('/posts/<int:id>...return')
@is_moderator
def returnPost_page(id):
    form = AddNotice_form()
    post = Post.query.get(id)
    posts = Post.query.filter_by(state='moderation')
    comments = Comment.query.filter_by(state='moderation')

    return create_response(template='moderator/noticePost_form.html', data={
        'title_page': 'Страница формы уведомления',
        'form': form,
        'post': post,
        'comments': comments,
        'posts': posts
    })


@moderator.route('/comments')
@is_moderator
def comments_page():
    comments = Comment.query.filter_by(state='moderation')
    posts = Post.query.filter_by(state='moderation')

    return create_response(template='moderator/comments.html', data={
        'title_page': 'Страница модерации комментариев',
        'comments': comments,
        'posts': posts
    })


@moderator.route('/coments/<int:id>')
@is_moderator
def comment_page(id):
    comment = Comment.query.get_or_404(id)
    comments = Comment.query.filter_by(state='moderation')
    posts = Post.query.filter_by(state='moderation')

    if comment.state == 'public':
        state_body = 'Опубликован'
    if comment.state == 'develop':
        state_body = 'Находится на доработке'
    if comment.state != 'moderation':
        return create_response(template='state.html', data={
            'title_page': 'Стадия контента',
            'state_title': 'Комментарий',
            'state_body': state_body
        })
    else:
        return create_response(template='moderator/comment.html', data={
            'title_page': 'Страница модерации комментария',
            'comment': comment,
            'comments': comments,
            'posts': posts
        })


@moderator.route('/comments/<int:id>...return')
@is_moderator
def returnComment_page(id):
    form = AddNotice_form()
    comment = Comment.query.get_or_404(id)
    posts = Post.query.filter_by(state='moderation')
    comments = Comment.query.filter_by(state='moderation')

    return create_response(template='moderator/noticeComment_form.html', data={
        'title_page': 'Страница формы уведомления',
        'form': form,
        'comment': comment,
        'posts': posts,
        'comments': comments
    })