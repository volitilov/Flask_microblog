# comment/req.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import redirect, request, url_for, flash

from flask_login import current_user, login_required

from . import comment
from .forms import AddComment_form
from ..models.post import Post
from ..models.comment import Comment
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
		flash(message='Ваш комментарий опубликован.', category='success')
		return redirect(url_for('post.post_page', id=post_id))



@comment.route(rule='/<int:comment_id>...edit', methods=['POST'])
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



@comment.route(rule='/<int:comment_id>...del')
@login_required
def delComment_request(comment_id):
	comment = Comment.query.get_or_404(comment_id)
	db.session.delete(comment)
	db.session.commit()
	flash(message='Ваш комментарий успешно удалён.', category='success')
	return redirect(url_for('comment.comments_page', username=comment.author.name))
