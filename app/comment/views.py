# comment/views.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import redirect, request, url_for, flash

from flask_login import current_user, login_required

from . import comment
from .forms import AddComment_form
from ..models.post import Post
from ..models.user import User
from ..models.comment import Comment
from ..utils import create_response
from .. import db

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@comment.route(rule='/...add-comment-to-post-<int:post_id>')
@login_required
def addComment_page(post_id):
	form = AddComment_form()
	post = Post.query.get_or_404(post_id)

	return create_response(template='comment/add_comment.html', data={
		'page_title': 'Страница добавления комментария',
		'post': post,
		'all_posts_count': Post.query.filter_by(state='public').count(),
        'followed_posts_count': current_user.followed_posts.filter(Post.state=='public').count(),
		'form': form
	})


@comment.route(rule='/<username>/comments/')
def comments_page(username):
	'''Генерирует страницу с комментариями пользователя.'''
	user = User.query.filter_by(name=username).first()
	if current_user == user:
		posts = user.posts.filter(Post.state!='moderator')
		comments = user.comments.filter(Comment.state!='moderation')
	else:
		posts = user.posts.filter_by(state='public')
		comments = user.comments.filter_by(state='public')
	sorted_comments = comments.order_by(Comment.timestamp.desc())

	return create_response(template='comment/comments.html', data={
		'page_title': 'Страница с комментариями пользователя.',
		'page': 'comments',
		'comments': sorted_comments,
		'posts': posts,
		'user': user
	})


@comment.route(rule='/<int:id>')
def comment_page(id):
	'''Генерирует страница для запрошенного комментария.'''
	comment = Comment.query.get_or_404(id)

	if comment.state == 'public' or \
		comment.state == 'develop' and comment.author == current_user:
			return create_response(template='comment/comment.html', data={
				'page_title': 'Страница комментария',
				'comment': comment,
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
				'state_body': state_body
			})



@comment.route(rule='/<int:comment_id>...edit')
@login_required
def editComment_page(comment_id):
	comment = Comment.query.get_or_404(comment_id)
	form = AddComment_form()

	if current_user != comment.author:
		flash(category='warn', 
			message='У вас не достаточно прав для редактирования комментария')
		return redirect(url_for('comment.comment_page', id=comment.id))
	else:
		form.body.data = comment.body

		return create_response(template='comment/edit_comment.html', data={
			'page_title': 'Страница редпктирования коментария',
			'form': form,
			'comment': comment,
			'user': comment.author
		})

