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
		'form': form
	})


@comment.route(rule='/<username>/comments/')
def comments_page(username):
	'''Генерирует страницу с комментариями пользователя.'''
	user = User.query.filter_by(name=username).first()
	posts = user.posts.filter(Post.moderation==True)
	sorted_comments = user.comments.order_by(Comment.timestamp.desc())

	return create_response(template='comment/comments.html', data={
		'page_title': 'Страница с комментариями пользователя.',
		'page': 'comments',
		'comments': sorted_comments.all(),
		'posts_count': posts.count(),
		'user': user
	})


@comment.route(rule='/<int:id>')
def comment_page(id):
	'''Генерирует страница для запрошенного комментария.'''
	comment = Comment.query.get_or_404(id)

	return create_response(template='comment/comment.html', data={
		'page_title': 'Страница комментария',
		'comment': comment,
		'user': comment.author
	})


@comment.route(rule='/<int:comment_id>...edit')
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

