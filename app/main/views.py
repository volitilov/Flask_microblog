# main/views.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import render_template, request, current_app

# flask extensions

# 
from . import main
from ..models import Post

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@main.route('/')
def home_page():
	'''Генерирует стартовую страницу.'''
	page = request.args.get('page', 1, type=int)
	pagination = Post.query.order_by(Post.data_creation.desc()).paginate(
		page, per_page=current_app.config['FLASKY_POST_PER_PAGE'], 
		error_out=False)
	data = {
		'page_title': 'Главная страница.',
		'posts': pagination.items,
		'pagination': pagination
	}
	return render_template('index.html', data=data)
