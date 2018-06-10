# user/views.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import (
	render_template, redirect, request, url_for, flash, session, abort
)

from flask_login import current_user, login_required, fresh_login_required

from . import post
from .forms import AddPost_form, AddComment_form
from ..models.post import Post
from ..models.user import User
from ..models.comment import Comment
from ..email import send_email
from ..utils import create_response
from .. import db

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@post.route(rule='/add_post', methods=['GET', 'POST'])
@fresh_login_required
def addPost_page():
	'''Генерирует страницу с формай создания постов.'''
	form = AddPost_form()
	data = {
		'page_title': 'Страница добавления поста.',
		'form': form,
	}

	if form.validate_on_submit():
		title = form.title.data
		text = form.text.data
		
		post = Post(title=title, text=text, author=current_user)
		db.session.add(post)
		db.session.commit()

		flash('Пост: <b>{}</b> - добавлен'.format(title))
		return redirect(url_for('main.home_page'))

	return create_response(template='post/add_post.html', data=data)


@post.route(rule='/users/<username>/posts')
def userPosts_page(username):
	'''Генерирует страницу с публикациями пользователя.'''
	user = User.query.filter_by(name=username).first()
	sorted_posts = user.posts.order_by(Post.data_creation.desc())

	data = {
		'page_title': 'Страница с публикациями пользователя.',
		'posts': sorted_posts.all()
	}

	return create_response(template='post/user_posts.html', data=data)


@post.route(rule='/post/<int:id>', methods=['GET', 'POST'])
def post_page(id):
	'''Генерирует страницу запрошенного поста'''
	post = Post.query.get_or_404(id)
	form = AddComment_form()

	data = {
		'page_title': post.title,
		'post': post,
		'form': form,
		'comments': post.comments
	}

	if form.validate_on_submit():
		body = form.body.data

		comment = Comment(body=body, post=post, author=current_user)
		db.session.add(comment)
		db.session.commit()
		flash('Ваш комментарий опубликован.')
		return redirect(url_for('post.post_page', id=id))

	return create_response(template='post/post.html', data=data)


@post.route(rule='/post/edit/<int:id>', methods=['GET', 'POST'])
@fresh_login_required
def editPost_page(id):
	'''Генерирует страницу редактирования поста.'''
	form = AddPost_form()
	post = Post.query.get_or_404(id)

	# form.title.data = post.title
	# form.text.data = post.body_html or post.text
	
	data = {
		'page_title': 'Страница редактирования поста',
		'form': form,
		'post': post
	}
	if form.validate_on_submit():
		post.title = form.title.data
		post.text = form.text.data

		db.session.add(post)
		db.session.commit()

		flash('Пост успешно сохранён.')
		return redirect(url_for('post.editPost_page', id=post.id))
	
	form.text.data = post.text

	return create_response(template='post/edit_post.html', data=data)


@post.route(rule='/delete_post/<int:id>', methods=['POST'])
@fresh_login_required
def deletePost_request(id):
	post = Post.query.get(id)
	db.session.delete(post)
	db.session.commit()
	return redirect(url_for('main.home_page'))