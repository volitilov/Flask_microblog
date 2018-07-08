# post/req.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import redirect, request, url_for, flash, current_app

from flask_login import current_user, login_required

from . import post
from .forms import AddPost_form
from ..models.user import User
from ..models.post import Post
from ..models.tag import Tag, Rel_tag
from ..models.post_rating import Post_rating
from .. import db

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@post.route(rule='/...add', methods=['POST'])
@login_required
def addPost_request():
	'''Обрабатывает запрос на добавление публикации'''
	form = AddPost_form()
	client = current_app.memory

	if form.validate_on_submit():
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
			
			all_tags.append(tag)
			rel_tags.append(Rel_tag(post=post, tag=tag))

		db.session.add_all([post, all_tags, rel_tags])
		db.session.commit()

		res = int(client.get(key='post_count'))
		res += 1
		client.set(key='post_count', value=res)

		flash(message='Пост успешно добавлен', category='success')
		return redirect(url_for(endpoint='main.home_page'))
	
	else:
		flash(category='error', message='Неправильно заполнена форма')
		return redirect(url_for('post.addPost_page'))



@post.route(rule='/<int:id>/...edit', methods=['POST'])
@login_required
def editPost_request(id):
	'''Обрабатывает запрос на изменение публикации'''
	form = AddPost_form()
	post = Post.query.get_or_404(id)
	
	if form.validate_on_submit():
		post.tags.delete()
		post.title = form.title.data
		post.table_of_contents = form.contents.data

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

		flash(message='Пост успешно сохранён.', category='success')
		return redirect(url_for('post.editPost_page', id=post.id))
	
	else:
		flash(category='error', message='Неверные данные')
		return redirect(url_for('post.editPost_page', id=post.id))



@post.route(rule='/<int:id>/...del')
@login_required
def deletePost_request(id):
	post = Post.query.get(id)

	db.session.delete(post)
	db.session.commit()
	
	client = current_app.memory
	res = int(client.get(key='post_count'))
	res -= 1
	client.set(key='post_count', value=res)

	flash(message='Пост успешно удалён', category='success')
	return redirect(url_for('post.posts_page'))



@post.route(rule='/<int:id>/...change_rating')
@login_required
def changeRating_request(id):
	post = Post.query.get_or_404(id)
	post.views -= 1
	
	rating = Post_rating(post=post, author=current_user)
	post.rating = post.ratings.count()
	db.session.add_all([rating, post])
	db.session.commit()

	flash(message='Ваше мнение учтенно.', category='success')
	return redirect(url_for('post.post_page', id=id))