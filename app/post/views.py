# -*- coding: utf-8 -*-
# post/views.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from functools import wraps

from flask import (
	request, flash, current_app, url_for, redirect
)

from flask_login import current_user, login_required

from . import post
from .utils import create_response
from .forms import AddPost_form
from .data import get_posts, page_titles
from ..models.post import Post
from ..models.user import User
from ..models.comment import Comment
from ..models.post_rating import Post_rating
from ..models.tag import Tag, Rel_tag
from .. import db

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

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


@post.route(rule='/posts/...add', methods=['GET', 'POST'])
@login_required
def addPost_page():
	'''Генерирует страницу с формай создания постов.'''
	data = get_posts()
	form = AddPost_form()
	client = current_app.memory

	if form.validate_on_submit():
		form.validate_title(form.title)
		title = form.title.data
		contents = form.contents.data
		text = form.text.data

		post = Post(title=title, table_of_contents=contents, text=text, 
			author=current_user)
		
		all_tags = []
		rel_tags = []
		form_tags = form.tags.data.split(',')
		for tag in form_tags:
			tag_name = tag.strip(' ')
			tag = Tag.query.filter_by(name=tag_name).first()
			if not tag:
				tag = Tag(name=tag_name)
			
			rel_tag = Rel_tag.query.filter_by(post=post, tag=tag).first()
			if not rel_tag:
				rel_tag = Rel_tag(post=post, tag=tag)

			all_tags.append(tag)
			rel_tags.append(rel_tag)

		db.session.add(post)
		db.session.add_all(all_tags)
		db.session.add_all(rel_tags)
		db.session.commit()

		flash(message='Пост отправлен на модерацию')
		return redirect(url_for(endpoint='main.home_page'))

	return create_response(template='post/add_post.html', data={
		'page_title': page_titles['addPost_page'],
		'form': form,
		'all_posts': data['all_posts'],
		'followed_posts': data['followed_posts']
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
			comments = user.comments.filter(Comment.state!='moderator')

	page = request.args.get('page', 1, type=int)
	pagination = posts.order_by(Post.data_creation.desc()).paginate(
		page, per_page=count_items, error_out=False)

	return create_response(template='post/user_posts.html', data={
		'page_title': page_titles['userPosts_page'],
		'page': 'user_posts',
		'posts': pagination.items,
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
		} for item in pagination.items]

	flash(category='success', 
		message='Показаны результаты запроса по тегу <b>{}</b>'.format(tag.name))

	return create_response(template='post/posts.html', data={
		'page_title': page_titles['tagPosts_page'],
		'page_posts': tag_posts,
		'pagination': pagination,
		'endpoint': 'post.tagPosts_page',
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
		if Post_rating.query.filter_by(post=post).filter_by(author=current_user).first():
			rating_bool = True

		if post.author == current_user:
			rating_bool = True

	if post.state == 'public' or \
		post.state == 'develop' and post.author == current_user:
			return create_response(template='post/post.html', data={
				'page_title': page_titles['post_page'] + post.title,
				'post': post,
				'comments': post.comments.filter(Comment.state=='public'),
				'rating_bool': rating_bool,
				'tags': tags,
				'all_posts': data['all_posts'],
				'followed_posts': data['followed_posts']
			})
	else:
		if post.state == 'moderation':
			state_body = 'Находится на модерации'
		if post.state == 'develop':
			state_body = 'Находится на доработке'
		if post.state != 'public':
			return create_response(template='state.html', data={
				'page_title': 'Стадия контента',
				'state_title': 'Пост',
				'state_body': state_body
			})


@post.route(rule='/posts/<int:id>/...edit')
@login_required
def editPost_page(id):
	'''Генерирует страницу редактирования поста.'''
	data = get_posts()
	form = AddPost_form()
	post = Post.query.get_or_404(id)
	
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


@post.route(rule='/posts/by_viewing/')
def byViewingPosts_page():
	'''Формирует страницу постов отсортированных по кол-ву просмотров.'''
	data = get_posts()
	count_items = current_app.config['APP_POSTS_PER_PAGE']

	page = request.args.get('page', 1, type=int)
	pagination = data['all_posts'].paginate(page, 
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
	pagination = data['all_posts'].paginate(page, 
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