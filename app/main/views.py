# main/views.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import render_template

# flask extensions

# 
from . import main
from ..models import Post

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@main.route('/')
def home_page():
	'''Генерирует стартовую страницу.'''
	data = {
		'page_title': 'Главная страница.',
		'posts': Post.query.order_by(Post.data_creation.desc()).all()
	}
	return render_template('index.html', data=data)
