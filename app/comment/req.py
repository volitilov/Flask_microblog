# comment/req.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import redirect, request, url_for, flash

from flask_login import current_user, login_required

from . import comment
from .forms import AddComment_form
from ..models.post import Post
from ..models.comment import Comment
from ..models.notice import Notice
from ..models.user_settings import UserSettings
from .. import db

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


@comment.route(rule='/<int:post_id>...add', methods=['POST'])
@login_required
def addComment_request(post_id):
	form = AddComment_form()
	post = Post.query.get_or_404(post_id)

	if form.validate_on_submit():
		body = form.body.data

		comment = Comment(body=body, post=post, author=current_user)
		
		db.session.add(comment)
		db.session.commit()
		flash(message='Ваш комментарий отправлен на модерацию.')
		return redirect(url_for('post.post_page', id=post_id))



@comment.route(rule='/<int:comment_id>...edit', methods=['POST'])
@login_required
def editComment_request(comment_id):
	comment = Comment.query.get_or_404(comment_id)
	form = AddComment_form()

	if current_user == comment.author:
		if form.validate_on_submit():
			comment.body = form.body.data
			comment.state = 'moderation'

			db.session.add(comment)
			db.session.commit()
			flash(message='Ваш комментарий отправлен на модерацию')
	else:
		flash(category='warn', message='Вы не являетесь автором комментария')
	
	return redirect(url_for('comment.comment_page', id=comment.id))



@comment.route(rule='/<int:comment_id>...del')
@login_required
def delComment_request(comment_id):
	comment = Comment.query.get_or_404(comment_id)

	if current_user == comment.author:
		db.session.delete(comment)
		db.session.commit()
		flash(message='Ваш комментарий успешно удалён.', category='success')
	else:
		flash(category='warn', 
			message='У вас не достаточно прав для удаления данного контента')
	return redirect(url_for('comment.comments_page', username=comment.author.name))
