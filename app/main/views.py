# views.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import (
	render_template, redirect, request, url_for, flash, session, abort
)

# flask extensions
from flask_mail import Message
from flask_login import current_user

# 
from . import main
from .forms import AddPost_form
from ..models import Post, User
from ..email import send_email
from .. import db

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@main.route('/')
def home_page():
	'''Генерирует стартовую страницу.'''
	data = {
		'page_title': 'Главная страница.'
	}
	return render_template('index.html', data=data)



@main.route('/add_post', methods=['GET', 'POST'])
def addPost_page():
	'''Генерирует страницу с формай создания постов.'''
	form = AddPost_form(request.form)
	data = {
		'page_title': 'Страница добавления поста.',
		'form': form,
	}

	if form.validate():
		title = form.title.data
		text = form.text.data
		
		post = Post(title=title, text=text)
		db.session.add(post)
		db.session.commit()

		send_email('otivito@mail.ru', 'Добавлен пост.', 'mail/new_post/add_post', 
                    title=title, text=text)

		data['post'] = {
			'title': title,
			'text': text
		}

		flash('Пост: <b>{}</b> - добавлен'.format(title))
		return redirect(url_for('main.home_page'))

	return render_template('add_post.html', data=data)



@main.route('/user/<name>')
def profile_page(name):
	'''Генерирует страницу профиля пользователя.'''
	data = {
		'page_title': 'Страница профиля',
		'date_registration': current_user.date_registration.strftime('%Y/%m/%d %H:%M:%S')
	}
	user = User.query.filter_by(name=name).first()
	if user is None:
		abort(404)

	return render_template('profile.html', data=data)

