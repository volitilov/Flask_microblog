# comment/forms.py

# Файл для работы с форммами

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.validators import Length

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class AddComment_form(FlaskForm):
	'''Форма добавления комментария.'''
	body = TextAreaField(label='Текст комментария', validators=[
		Length(min=10, max=5000, 
			message='Комментарий не должен быть меньше 10 и больше 5000 символов')])
