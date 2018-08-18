# comment/routes/reqs.py

# Обрабатывает POST-запросы 
# Работа с данными: добавление, редактирование, удаление

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import redirect, request, url_for, flash, abort
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

@comment.route(rule='/comments/<int:comment_id>...del')
@login_required
def delComment_request(comment_id):
	comment = Comment.query.get_or_404(comment_id)

	if current_user != comment.author:
		abort(403)
	
	db.session.delete(comment)
	db.session.commit()
	flash(message='Ваш комментарий успешно удалён.', category='success')
	return redirect(url_for('comment.comments_page', username=comment.author.name))
