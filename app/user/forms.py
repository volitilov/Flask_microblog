# user/forms.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask_wtf import FlaskForm
from wtforms import (
	StringField, TextAreaField, PasswordField, ValidationError
)
from wtforms.validators import (
	DataRequired, Email, Length, EqualTo, Regexp
)
from ..models import User

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class EditProfile_form(FlaskForm):
	'''Форма редактирования профиля'''
	first_name = StringField(label='Имя:', validators=[DataRequired()])
	last_name = StringField(label='Фамилия:', validators=[DataRequired()])
	about = TextAreaField(label='Обо мне:', validators=[DataRequired()])
	location = StringField(label='Местоположение:', validators=[DataRequired()])


class ChangeEmail_form(FlaskForm):
    email = StringField(label='Новый email', 
        validators=[DataRequired(), Email(), Length(5, 64)])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Данный email уже есть.')


class ChangeLogin_form(FlaskForm):
	'''Форма изменения логина'''
	name = StringField(label='Новый login', 
		validators=[DataRequired(), Length(1, 64), 
			Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 
        		'''Имена пользователей должны иметь только числа, 
					точки или символы подчеркивания''')])
	

class ChangePassword_form(FlaskForm):
	old_password = PasswordField(label='Старый пароль', 
		validators=[DataRequired()])
	password = PasswordField(label='Новый пароль', 
		validators=[DataRequired(), EqualTo('password2', 
			message='Пароли должны совпадать.')])
	password2 = PasswordField(label='Повторите пароль',
        validators=[DataRequired()])