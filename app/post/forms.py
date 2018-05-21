# post/forms.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_pagedown.fields import PageDownField

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class AddPost_form(FlaskForm):
	'''Форма добавления постов'''
	title = StringField(label='title', validators=[DataRequired()])
	text = PageDownField(label='text for post', validators=[DataRequired()])
