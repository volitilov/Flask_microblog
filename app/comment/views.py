# comment/views.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import redirect, request, url_for, flash

from flask_login import current_user, login_required

from . import comment
from .utils import create_response
from .forms import AddComment_form
from .data import page_titles, get_data
from ..models.post import Post
from ..models.user import User
from ..models.comment import Comment
from .. import db

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@comment.route(rule='/comments/...add-comment-to-post-<int:id>')
@login_required
def addComment_page(id):
	'''Генерирует страницу для добавления комментария'''
	return create_response(template='comment/add_comment.html', data={
		'page_title': page_titles['addComment_page'],
		'post': Post.query.get_or_404(id),
		'all_posts': Post.query.filter_by(state='public'),
        'followed_posts': current_user.followed_posts.filter(Post.state=='public'),
		'form': AddComment_form()
	})


@comment.route(rule='/<username>/comments/')
def comments_page(username):
	'''Генерирует страницу с комментариями пользователя.'''
	user = User.query.filter_by(name=username).first()
	data = get_data(current_user, user)

	comments = data['comments'].order_by(Comment.timestamp.desc())

	return create_response(template='comment/comments.html', data={
		'page_title': page_titles['comments_page'],
		'page': 'comments',
		'comments': comments,
		'posts': data['posts'],
		'user': user
	})


@comment.route(rule='/comments/<int:id>')
def comment_page(id):
	'''Генерирует страница для запрошенного комментария.'''
	comment = Comment.query.get_or_404(id)
	user = comment.author
	data = get_data(current_user, user)

	if comment.state == 'public' or \
		comment.state == 'develop' and user == current_user:
			return create_response(template='comment/comment.html', data={
				'page_title': page_titles['comment_page'],
				'comment': comment,
				'posts': data['posts'],
				'comments': data['comments'],
				'user': comment.author
			})
	else:
		if comment.state == 'moderation':
			state_body = 'Находится на модерации'
		if comment.state == 'develop':
			state_body = 'Находится на доработке'
		if comment.state != 'public':
			return create_response(template='state.html', data={
				'page_title': 'Стадия контента',
				'state_title': 'Комментарий',
				'posts': data['posts'],
				'followed_posts': current_user.followed_posts.filter(Post.state=='public'),
				'state_body': state_body
			})



@comment.route(rule='/<username>/comments/<int:comment_id>...edit')
@login_required
def editComment_page(username, comment_id):
	'''Генерирует страницу редактирования комментария'''
	comment = Comment.query.get_or_404(comment_id)
	form = AddComment_form()
	user = comment.author
	data = get_data(current_user, user)

	if current_user != user or comment.state == 'moderation':
		flash(category='warn', 
			message='На данный момент у вас не достаточно прав для редактирования комментария')
		return redirect(url_for(
			endpoint='comment.comment_page', 
			username=current_user.name, 
			id=comment.id))
	else:
		form.body.data = comment.body
		return create_response(template='comment/edit_comment.html', data={
			'page_title': page_titles['editComment_page'],
			'form': form,
			'comment': comment,
			'user': user,
			'posts': data['posts'],
			'comments': data['comments']
		})

