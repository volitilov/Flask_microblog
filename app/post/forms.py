# post/forms.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class AddPost_form(FlaskForm):
	'''Форма добавления постов'''
	title = StringField(label='title', validators=[DataRequired()])
	text = TextAreaField(label='text for post', validators=[DataRequired()])
