# post/views.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import (
	request, flash, current_app, url_for
)

from flask_login import current_user, login_required

from . import post
from .forms import AddPost_form
from ..models.post import Post
from ..models.user import User
from ..models.comment import Comment
from ..utils import create_response
from .. import db

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@post.route('/followed_posts')
@login_required
def followedPosts_page():
	count_items = current_app.config['APP_POSTS_PER_PAGE']
	posts = current_user.followed_posts
	page = request.args.get('page', 1, type=int)
	pagination = posts.order_by(Post.data_creation.desc()).paginate(
		page, per_page=count_items, error_out=False)

	return create_response(template='index.html', data={
		'page_title': 'Публикации по подписке',
		'pagination': pagination,
		'posts': pagination.items,
		'page': 'followed_posts',
		'endpoint': 'post.followedPosts_page',
		'posts_count': posts.count(),
		'posts_per_page': count_items
	})


@post.route(rule='/...add')
@login_required
def addPost_page():
	'''Генерирует страницу с формай создания постов.'''

	return create_response(template='post/add_post.html', data={
		'page_title': 'Страница добавления поста.',
		'form': AddPost_form()
	})


@post.route(rule='/<username>/posts/')
def posts_page(username):
	'''Генерирует страницу с публикациями пользователя.'''
	user = User.query.filter_by(name=username).first()
	count_items = current_app.config['APP_POSTS_PER_PAGE']

	page = request.args.get('page', 1, type=int)
	pagination = user.posts.order_by(Post.data_creation.desc()).paginate(
		page, per_page=count_items, error_out=False)


	return create_response(template='post/posts.html', data={
		'page_title': 'Страница с публикациями пользователя.',
		'page': 'posts',
		'posts': pagination.items,
		'pagination': pagination,
		'endpoint': 'post.posts_page',
		'user': user,
		'posts_count': user.posts.count(),
		'posts_per_page': count_items
	})


@post.route(rule='/<int:id>')
def post_page(id):
	'''Генерирует страницу запрошенного поста'''
	post = Post.query.get_or_404(id)
	post.views += 1

	db.session.add(post)
	db.session.commit()

	return create_response(template='post/post.html', data={
		'page_title': post.title,
		'post': post,
		'comments': post.comments
	})


@post.route(rule='/<int:id>/...edit')
@login_required
def editPost_page(id):
	'''Генерирует страницу редактирования поста.'''
	form = AddPost_form()
	post = Post.query.get_or_404(id)
	
	form.text.data = post.text

	return create_response(template='post/edit_post.html', data={
		'page_title': 'Страница редактирования поста',
		'form': form,
		'post': post
	})


@post.route(rule='/by_viewing')
def byViewingPosts_page():
	'''Формирует страницу постов отсортированных по кол-ву просмотров.'''
	posts = Post.query.order_by(Post.views.desc())
	count_items = current_app.config['APP_POSTS_PER_PAGE']

	page = request.args.get('page', 1, type=int)
	pagination = posts.paginate(page, per_page=count_items, error_out=False)

	return create_response(template='index.html', data={
		'page_title': 'Публикации по кол-ву просмотров.',
		'page': 'post_views',
		'posts': pagination.items,
		'pagination': pagination,
		'endpoint': 'post.byViewingPosts_page',
		'posts_count': posts.count(),
		'posts_per_page': count_items
	})
