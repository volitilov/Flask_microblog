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
from ..models.post_rating import Post_rating
from ..models.tag import Tag
from ..utils import create_response
from .. import db

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@post.route('/')
def posts_page():
	'''Генерирует страницу со всеми публикациями.'''
	count_items = current_app.config['APP_POSTS_PER_PAGE']
	posts = Post.query.order_by(Post.data_creation.desc())
	
	page = request.args.get('page', 1, type=int)
	pagination = posts.paginate(
		page, per_page=count_items, error_out=False)

	return create_response(template='post/posts.html', data={
		'page_title': 'Cтраница со всеми публикациями.',
		'pagination': pagination,
		'posts': pagination.items,
		'endpoint': 'post.posts_page',
		'page': 'all_posts',
		'posts_count': posts.count(),
		'posts_per_page': count_items
	})


@post.route('/followed_posts')
@login_required
def followedPosts_page():
	'''Создаёт страницу с побликациями пользователей на которых подписан
	текущий пользователь'''
	count_items = current_app.config['APP_POSTS_PER_PAGE']
	posts = current_user.followed_posts
	page = request.args.get('page', 1, type=int)
	pagination = posts.order_by(Post.data_creation.desc()).paginate(
		page, per_page=count_items, error_out=False)

	return create_response(template='post/posts.html', data={
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
def userPosts_page(username):
	'''Генерирует страницу с публикациями пользователя.'''
	user = User.query.filter_by(name=username).first()
	count_items = current_app.config['APP_POSTS_PER_PAGE']

	page = request.args.get('page', 1, type=int)
	pagination = user.posts.order_by(Post.data_creation.desc()).paginate(
		page, per_page=count_items, error_out=False)

	return create_response(template='post/user_posts.html', data={
		'page_title': 'Страница с публикациями пользователя.',
		'page': 'user_posts',
		'posts': pagination.items,
		'pagination': pagination,
		'endpoint': 'post.userPosts_page',
		'user': user,
		'posts_count': user.posts.count(),
		'posts_per_page': count_items
	})


@post.route(rule='/tag/<int:id>/')
def tagPosts_page(id):
	'''Генерирует страницу с публикациями по запрошенному тегу.'''
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
		} for item in pagination.items]

	flash(category='success', 
		message='Показаны результаты запроса по тегу <b>{}</b>'.format(tag.name))

	return create_response(template='post/posts.html', data={
		'page_title': 'Страница с публикациями по запрошенному тегу.',
		'posts': tag_posts,
		'pagination': pagination,
		'endpoint': 'post.tagPosts_page',
		'posts_count': posts.count(),
		'posts_per_page': count_items,
		'tag': tag
	})


@post.route(rule='/<int:id>')
def post_page(id):
	'''Генерирует страницу запрошенного поста'''
	post = Post.query.get_or_404(id)
	tags = post.tags.all()
	post.views += 1

	db.session.add(post)
	db.session.commit()

	rating_bool = False
	
	if Post_rating.query.filter_by(post=post).filter_by(author=current_user).first():
		rating_bool = True

	if post.author == current_user:
		rating_bool = True

	return create_response(template='post/post.html', data={
		'page_title': post.title,
		'post': post,
		'comments': post.comments,
		'rating_bool': rating_bool,
		'tags': tags
	})


@post.route(rule='/<int:id>/...edit')
@login_required
def editPost_page(id):
	'''Генерирует страницу редактирования поста.'''
	form = AddPost_form()
	post = Post.query.get_or_404(id)
	
	form.text.data = post.text
	form.contents.data = post.table_of_contents

	tags = []
	for rel_tag in post.tags.all():
		tags.append(rel_tag.tag.name)
	form.tags.data = ', '.join(tags)

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

	return create_response(template='post/posts.html', data={
		'page_title': 'Публикации по кол-ву просмотров.',
		'page': 'post_views',
		'posts': pagination.items,
		'pagination': pagination,
		'endpoint': 'post.byViewingPosts_page',
		'posts_count': posts.count(),
		'posts_per_page': count_items
	})


@post.route(rule='/by_rating')
def byRatingPosts_page():
	'''Формирует страницу постов отсортированных по рейтингу.'''
	posts = Post.query.order_by(Post.rating.desc())
	count_items = current_app.config['APP_POSTS_PER_PAGE']

	page = request.args.get('page', 1, type=int)
	pagination = posts.paginate(page, per_page=count_items, error_out=False)

	return create_response(template='post/posts.html', data={
		'page_title': 'Публикации по рейтингу.',
		'page': 'post_ratings',
		'posts': pagination.items,
		'pagination': pagination,
		'endpoint': 'post.byRatingPosts_page',
		'posts_count': posts.count(),
		'posts_per_page': count_items
	})