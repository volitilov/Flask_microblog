# post/forms.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_pagedown.fields import PageDownField

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class AddPost_form(FlaskForm):
	'''Форма добавления поста.'''
	title = StringField(label='Загаловок поста', validators=[DataRequired()])
	text = PageDownField(label='Текст поста', validators=[DataRequired()])
