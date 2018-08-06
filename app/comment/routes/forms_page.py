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
