# main/views.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import render_template

# flask extensions

# 
from . import main

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@main.route('/')
def home_page():
	'''Генерирует стартовую страницу.'''
	data = {
		'page_title': 'Главная страница.'
	}
	return render_template('index.html', data=data)
