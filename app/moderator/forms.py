# moderator/forms.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from flask_pagedown.fields import PageDownField

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class AddNotice_form(FlaskForm):
	'''Форма добавления уведомления.'''
	body = PageDownField(label='Текст уведомления', 
		validators=[DataRequired()])

