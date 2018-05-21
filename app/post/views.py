# user/views.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import (
	render_template, redirect, request, url_for, flash, session, abort
)

# flask extensions
from flask_login import current_user, login_required

# 
from . import post
from .forms import AddPost_form
from ..models.post import Post
from ..models.user import User
from ..email import send_email
from ..utils import create_response
from .. import db

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@post.route(rule='/add_post', methods=['GET', 'POST'])
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

		send_email('otivito@mail.ru', 'Добавлен пост.', 'mail/new_post/add_post', 
                    title=title, text=text)

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