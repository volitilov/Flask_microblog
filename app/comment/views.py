# comment/views.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import (
	redirect, request, url_for, flash, session
)

from flask_login import current_user, login_required

from . import comment
from .forms import AddComment_form
from ..models.post import Post
from ..models.user import User
from ..models.comment import Comment
from ..utils import create_response
from .. import db

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@comment.route(rule='/comments/add/<int:post_id>')
def addComment_page(post_id):
	form = AddComment_form()
	post = Post.query.get_or_404(post_id)

	return create_response(template='comment/add_comment.html', data={
		'page_title': 'Страница добавления комментария',
		'post': post,
		'form': form
	})


@comment.route(rule='/users/<username>/comments/')
def comments_page(username):
	'''Генерирует страницу с комментариями пользователя.'''
	user = User.query.filter_by(name=username).first()
	sorted_comments = user.comments.order_by(Comment.timestamp.desc())

	return create_response(template='comment/comments.html', data={
		'page_title': 'Страница с комментариями пользователя.',
		'comments': sorted_comments.all(),
		'user': user
	})


@comment.route(rule='/comments/<int:id>')
def comment_page(id):
	'''Генерирует страница для запрошенного комментария.'''
	comment = Comment.query.get_or_404(id)

	return create_response(template='comment/comment.html', data={
		'page_title': 'Страница комментария',
		'comment': comment,
		'user': comment.author
	})


@comment.route(rule='/req/comments/add/<int:post_id>', methods=['POST'])
@login_required
def addComment_request(post_id):
	form = AddComment_form()
	post = Post.query.get_or_404(post_id)

	if form.validate_on_submit():
		body = form.body.data

		comment = Comment(body=body, post=post, author=current_user)
		db.session.add(comment)
		db.session.commit()
		flash(message='Ваш комментарий опубликован.', category='success')
		return redirect(url_for('post.post_page', id=post_id))


@comment.route(rule='/comments/edit/<int:comment_id>')
@login_required
def editComment_page(comment_id):
	comment = Comment.query.get_or_404(comment_id)
	form = AddComment_form()

	form.body.data = comment.body

	return create_response(template='comment/edit_comment.html', data={
		'page_title': 'Страница редпктирования коментария',
		'form': form,
		'comment': comment,
		'user': comment.author
	})



@comment.route(rule='/req/comments/edit/<int:comment_id>', methods=['POST'])
@login_required
def editComment_request(comment_id):
	comment = Comment.query.get_or_404(comment_id)
	form = AddComment_form()

	if form.validate_on_submit():
		comment.body = form.body.data

		db.session.add(comment)
		db.session.commit()
		flash(message='Ваш комментарий успешно отредактирован.', category='success')
		return redirect(url_for('post.post_page', id=comment.post.id))



@comment.route(rule='/req/comments/delete/<int:comment_id>')
@login_required
def delComment_request(comment_id):
	comment = Comment.query.get_or_404(comment_id)
	db.session.delete(comment)
	db.session.commit()
	flash(message='Ваш комментарий успешно удалён.', category='success')
	return redirect(url_for('comment.comments_page', username=comment.author.name))
