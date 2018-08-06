# comment/req.py

# Обрабатывает POST-запросы 
# Работа с данными: добавление, редактирование, удаление

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import redirect, request, url_for, flash

from flask_login import current_user, login_required

from .. import (
	# bluprint
	comment,
	
	# forms
	AddComment_form,

	# models
	Post, Comment, Notice, UserSettings, 
	
	# database
	db
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


@comment.route(rule='/<username>/comments/<int:post_id>...add', methods=['POST'])
@login_required
def addComment_request(username, post_id):
	form = AddComment_form()
	post = Post.query.get_or_404(post_id)

	if form.validate_on_submit():
		body = form.body.data

		comment = Comment(body=body, post=post, author=current_user)

		user_settings = UserSettings.query.filter_by(state='custom', profile=comment.post.author).first()
		if user_settings.comments_me:
			notice_title = 'Оставили комментарий к посту'
			notice_body = '''<b>{}</b> - оставил вам комметарий к посту - 
				<b>{}</b><br><br>На данный момент он отправлен к вам на модерацию, 
				<a href="{}">посмотреть</a>'''.format(
					comment.author.name, comment.post.title, 
					url_for('user.adminComment_page', username=username, id=comment.id)
			)
			notice = Notice(title=notice_title, body=notice_body, author=comment.post.author)
			db.session.add(notice)
		
		db.session.add(comment)
		db.session.commit()
		flash(message='Ваш комментарий отправлен на модерацию.')
		return redirect(url_for('post.post_page', id=post_id))



@comment.route(rule='/<username>/comments/<int:comment_id>...edit', methods=['POST'])
@login_required
def editComment_request(username, comment_id):
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
	
	return redirect(url_for('comment.comment_page', username=current_user.name, id=comment.id))



@comment.route(rule='/<username>/comments/<int:comment_id>...del')
@login_required
def delComment_request(username, comment_id):
	comment = Comment.query.get_or_404(comment_id)

	if current_user == comment.author:
		db.session.delete(comment)
		db.session.commit()
		flash(message='Ваш комментарий успешно удалён.', category='success')
	else:
		flash(category='warn', 
			message='У вас не достаточно прав для удаления данного контента')
	return redirect(url_for('comment.comments_page', username=comment.author.name))
