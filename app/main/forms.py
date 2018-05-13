# main/forms.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from wtforms import Form, StringField, TextAreaField, PasswordField
from wtforms.validators import (
	DataRequired, Email, Length, EqualTo, Regexp
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class AddPost_form(Form):
	'''Форма добавления постов'''
	title = StringField(label='title', validators=[DataRequired()])
	text = TextAreaField(label='text for post', validators=[DataRequired()])


# class EditProfile_form(Form):
# 	'''Форма редактирования профиля'''
