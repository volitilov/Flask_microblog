# views.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import (
	render_template, redirect, request, url_for, flash, session
)

# flask extensions
from flask_mail import Message
from flask_login import current_user

# 
from . import main
from .forms import AddPost_form
from ..models import Post
from ..email import send_email
from .. import db

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@main.route('/')
def home_page():
	data = {
		'page_title': 'Главная страница.'
	}
	return render_template('index.html', data=data)


@main.route('/add_post', methods=['GET', 'POST'])
def addPost_page():
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


@main.route('/profile', methods=['GET', 'POST'])
def profile_page():
	data = {
		'page_title': 'Страница профиля',
		'name': current_user.name,
		'email': current_user.email,
		'confirmed': current_user.confirmed
	}

	return render_template('profile.html', data=data)

