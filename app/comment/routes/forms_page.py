# comment/routes/forms_page.py

# Обрабатывает страницы с формами

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import redirect, request, url_for, flash

from flask_login import current_user, login_required

from .. import (
	# blueprint
	comment,

	# utils
	create_response,

	# forms
	AddComment_form,

	# data 
	page_titles, get_data,
	
	# models 
	Post, User, Comment,

	# database
	db
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@comment.route(rule='/<username>/comments/...add-comment-to-post-<int:id>', methods=['GET', 'POST'])
@login_required
def addComment_page(username, id):
	'''Генерирует страницу для добавления комментария'''
	form = AddComment_form()
	post = Post.query.get_or_404(id)

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
		return redirect(url_for('post.post_page', id=id))

	return create_response(template='add_comment.html', data={
		'page_title': page_titles['addComment_page'],
		'post': Post.query.get_or_404(id),
		'all_posts': Post.query.filter_by(state='public'),
        'followed_posts': current_user.followed_posts.filter(Post.state=='public'),
		'form': form
	})



@comment.route(rule='/<username>/comments/<int:comment_id>...edit', methods=['GET', 'POST'])
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
		if form.validate_on_submit():
			comment.body = form.body.data
			comment.state = 'moderation'

			db.session.add(comment)
			db.session.commit()
			flash(message='Ваш комментарий отправлен на модерацию')

		form.body.data = comment.body
		return create_response(template='edit_comment.html', data={
			'page_title': page_titles['editComment_page'],
			'form': form,
			'comment': comment,
			'user': user,
			'posts': data['posts'],
			'comments': data['comments']
		})
