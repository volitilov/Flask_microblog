# post/forms.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, Regexp
from flask_pagedown.fields import PageDownField

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class AddPost_form(FlaskForm):
	'''Форма добавления поста.'''
	title = StringField(label='Загаловок поста', validators=[DataRequired()])
	text = PageDownField(label='Текст поста', validators=[DataRequired()])
	tags = StringField(label='Теги', 
		validators=[
			DataRequired(message='Теги указывать обязательно'), 
			Length(1, 64),
            Regexp('^[A-Za-z][A-Za-z0-9,\s]*$', 
			0, 
        	'Имена тегов должны иметь только буквы и числа,')])