# comment/forms.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_pagedown.fields import PageDownField

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class AddComment_form(FlaskForm):
	'''Форма добавления комментария.'''
	body = PageDownField(label='Комментарий', 
		validators=[DataRequired()])