# post/req.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import redirect, request, url_for, flash, current_app

from flask_login import current_user, login_required

from . import post
from .forms import AddPost_form
from ..models.user import User
from ..models.post import Post
from ..models.post_rating import Post_rating
from .. import db

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@post.route(rule='/...add', methods=['POST'])
@login_required
def addPost_request():
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



@post.route(rule='/<int:id>/...edit', methods=['POST'])
@login_required
def editPost_request(id):
	form = AddPost_form()
	post = Post.query.get_or_404(id)
	
	if form.validate_on_submit():
		post.title = form.title.data
		post.text = form.text.data

		db.session.add(post)
		db.session.commit()

		flash(message='Пост успешно сохранён.', category='success')
		return redirect(url_for('post.editPost_page', id=post.id))



@post.route(rule='/<int:id>/...del')
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



@post.route(rule='/<int:id>/...change_rating')
@login_required
def changeRating_request(id):
	post = Post.query.get_or_404(id)
	
	rating = Post_rating(post=post, author=current_user)
	db.session.add(rating)
	db.session.commit()

	flash(message='Ваше мнение учтенно.', category='success')
	return redirect(url_for('post.post_page', id=id))