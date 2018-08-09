# notice/forms.py

# Файл для работы с формами

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask_wtf import FlaskForm
from wtforms.validators import Length
from flask_pagedown.fields import PageDownField

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class AddNotice_form(FlaskForm):
	'''Форма добавления уведомления.'''
	body = PageDownField(label='Текст уведомления', validators=[
		Length(min=15, max=1000, 
			message='Уведомление не должено быть меньше 15, больше 1000 символов')])
