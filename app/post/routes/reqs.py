# post/routes/reqs.py

# Обрабатывает POST-запросы 
# Работа с данными: добавление, редактирование, удаление

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import redirect, url_for, flash, abort
from flask_login import current_user, login_required

from .. import (
	# blueprint
	post,

	# models
	Post, Post_rating, Tag, Rel_tag,

	# database
	db
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@post.route(rule='/posts/<int:id>...send_moderation')
@login_required
def sendModerationPost_request(id):
	'''Отправляет пост на модерацию.'''
	post = Post.query.get_or_404(id)
	post.state = 'moderation'
	db.session.add(post)
	db.session.commit()
	flash(message='Пост отправлен на модерацию.')
	return redirect(url_for('post.posts_page'))



@post.route(rule='/<int:id>/...del')
@login_required
def deletePost_request(id):
	post = Post.query.get_or_404(id)
	
	if current_user != post.author:
		abort(403)

	post_r = Post_rating.query.filter_by(post=post).all()
	for pr in post_r:
		db.session.delete(pr)

	rel_tags = Rel_tag.query.filter_by(post=post).all()
    for r_t in rel_tags:
        tag = r_t.tag
        tags = Tag.query.filter_by(name=tag.name).all()
        for t in tags:
            if t.posts.count() <= 1:
                db.session.delete(t)
        
        db.session.delete(r_t)

	db.session.delete(post)
	db.session.commit()
	flash(message='Пост успешно удалён', category='success')
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
	post.author.rating += 1
	db.session.add_all([rating, post])
	db.session.commit()

	flash(message='Ваше мнение учтенно.', category='success')
	return redirect(url_for('post.post_page', id=id))
