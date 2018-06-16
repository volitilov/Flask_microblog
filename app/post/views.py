# user/views.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import (
	render_template, redirect, request, url_for, flash, session, abort,
	current_app
)

from flask_login import current_user, login_required

from . import post
from .forms import AddPost_form
from ..models.post import Post
from ..models.user import User
from ..models.comment import Comment
from ..email import send_email
from ..utils import create_response
from .. import db

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@post.route(rule='/add_post', methods=['GET', 'POST'])
@login_required
def addPost_page():
	'''Генерирует страницу с формай создания постов.'''
	form = AddPost_form()
	client = current_app.memory

	if form.validate_on_submit():
		title = form.title.data
		text = form.text.data
		
		post = Post(title=title, text=text, author=current_user)
		db.session.add(post)
		db.session.commit()

		res = int(client.get(key='post_count'))
		res += 1
		client.set(key='post_count', value=res)

		flash(message='Пост успешно добавлен', category='success')
		return redirect(url_for(endpoint='main.home_page'))

	return create_response(template='post/add_post.html', data={
		'page_title': 'Страница добавления поста.',
		'form': form,
		'post_count': int(client.get(key='post_count'))
	})


@post.route(rule='/users/<username>/posts')
def posts_page(username):
	'''Генерирует страницу с публикациями пользователя.'''
	user = User.query.filter_by(name=username).first()
	sorted_posts = user.posts.order_by(Post.data_creation.desc())

	return create_response(template='post/posts.html', data={
		'page_title': 'Страница с публикациями пользователя.',
		'posts': sorted_posts.all(),
		'user': user,
		'post_count': int(current_app.memory.get(key='post_count'))
	})


@post.route(rule='/post/<int:id>')
def post_page(id):
	'''Генерирует страницу запрошенного поста'''
	post = Post.query.get_or_404(id)

	return create_response(template='post/post.html', data={
		'page_title': post.title,
		'post': post,
		'comments': post.comments,
		'post_count': int(current_app.memory.get(key='post_count'))
	})


@post.route(rule='/post/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def editPost_page(id):
	'''Генерирует страницу редактирования поста.'''
	form = AddPost_form()
	post = Post.query.get_or_404(id)
	
	if form.validate_on_submit():
		post.title = form.title.data
		post.text = form.text.data

		db.session.add(post)
		db.session.commit()

		flash(message='Пост успешно сохранён.', category='success')
		return redirect(url_for('post.editPost_page', id=post.id))
	
	form.text.data = post.text

	return create_response(template='post/edit_post.html', data={
		'page_title': 'Страница редактирования поста',
		'form': form,
		'post': post,
		'post_count': int(current_app.memory.get(key='post_count'))
	})


@post.route(rule='/delete_post/<int:id>')
@login_required
def deletePost_request(id):
	post = Post.query.get(id)
	
	client = current_app.memory
	res = int(client.get(key='post_count'))
	res -= 1
	client.set(key='post_count', value=res)

	db.session.delete(post)
	db.session.commit()

	flash(message='Пост успешно удалён', category='success')
	return redirect(url_for('main.home_page'))