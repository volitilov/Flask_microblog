# auth/routes/pages.py

# Обрабатывает GET-запросы
# Формирует страницы для запрошенных урлов 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import redirect, url_for
from flask_login import current_user

from .. import (
	# blueprint
	auth,

	# utils
	create_response,

	# data
	page_titles
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@auth.route(rule='/unconfirmed')
def unconfirmed_page():
	'''Генерирует страницу с предложением потвердить свою учетную запись'''
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for('main.home_page'))
	return create_response(template='unconfirmed.html', data={
		'page_title': page_titles['unconfirmed_page']
	})
