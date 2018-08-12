# post/routes/reqs.py

# Обрабатывает POST-запросы 
# Работа с данными: добавление, редактирование, удаление

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import redirect, url_for, flash
from flask_login import current_user, login_required

from .. import (
	# blueprint
	post,

	# models
	Post, Post_rating,

	# database
	db
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@post.route(rule='/<int:id>/...del')
@login_required
def deletePost_request(id):
	post = Post.query.get(id)

	if current_user == post.author:
		db.session.delete(post)
		db.session.commit()
		flash(message='Пост успешно удалён', category='success')
	else:
		flash(category='warn', message='У вас недостаточно прав на удаление')

	return redirect(url_for('post.posts_page'))



@post.route(rule='/<int:id>/...change_rating')
@login_required
def changeRating_request(id):
	post = Post.query.get_or_404(id)
	
	if Post_rating.query.filter_by(post=post).filter_by(author=current_user).first() \
		or post.author == current_user:
		flash(category='warn', message='Ваше мнение уже учтенно.')
		return redirect(url_for('post.post_page', id=id))
		
	post.views -= 1
	
	rating = Post_rating(post=post, author=current_user)
	post.rating = post.ratings.count()
	db.session.add_all([rating, post])
	db.session.commit()

	flash(message='Ваше мнение учтенно.', category='success')
	return redirect(url_for('post.post_page', id=id))
