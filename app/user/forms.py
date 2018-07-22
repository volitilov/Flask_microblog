# user/forms.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask_wtf import FlaskForm
from wtforms import (
	StringField, TextAreaField, PasswordField, ValidationError,
	BooleanField
)
from flask_pagedown.fields import PageDownField

from wtforms.validators import (
	DataRequired, Email, Length, EqualTo, Regexp, StopValidation
)
from flask_wtf.file import FileField, FileAllowed

from ..models.user import User
from .utils import FileSize

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class EditProfile_form(FlaskForm):
	'''Форма редактирования профиля'''
	first_name = StringField(label='Имя:', 
		validators=[Length(max=20, message='Максимальная длина 20 символов')])
	last_name = StringField(label='Фамилия:', 
		validators=[Length(max=30, message='Максимальная длина 30 символов')])
	about = PageDownField(label='Обо мне:', 
		validators=[Length(max=10000, message='Максимальное количество символов 10000')])
	location = StringField(label='Местоположение:',
		validators=[Length(max=20, message='Название местоположения не должно превышать 20 симв.')])
	photo = FileField(label='Фото', 
		validators=[
			FileSize(max=1*1024*1024, message='Максимальный размер 1мб.'),
			FileAllowed(
				upload_set=['jpg', 'png', 'jpeg', 'gif', 'svg'], 
				message='Поддерживаются следующие форматы: png, jpg, jpeg, gif, svg')])
	


class ChangeEmail_form(FlaskForm):
    email = StringField(label='', validators=[
		Email(message='Неверный email-адрес'), 
		Length(min=5, max=64, message='Email-адрес не должен быть меньше 5, больше 64 символов')])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(message='Данный email уже есть.')



class ChangeLogin_form(FlaskForm):
	'''Форма изменения логина'''
	name = StringField(label='', validators=[ 
		Length(min=5, max=20, message='Login не должен быть меньше 5, больше 20 символов'), 
		Regexp(regex='^[A-Za-z][A-Za-z0-9_.]*$', message='''Имена пользователей должны иметь только числа, 
				точки или символы подчеркивания''')])
	


class ChangePassword_form(FlaskForm):
	old_password = PasswordField(label='Старый пароль', validators=[
		DataRequired(message='Поле обязательно для заполнения')])

	password = PasswordField(label='Новый пароль', validators=[
		DataRequired(message='Поле обязательно для заполнения'),
		Length(min=3, max=64, message='Пароль не должен быть меньше 8 и больше 64 символов'),
		EqualTo(fieldname='password2', message='Пароли должны совпадать.')])

	password2 = PasswordField(label='Повторите пароль', validators=[
		DataRequired(message='Поле обязательно для заполнения')])



class EditNotice_form(FlaskForm):
	'''Форма настроек уведомлений.'''
	comments_me = BooleanField(label='оставили комментарий к посту')
	follow_me = BooleanField(label='подписались на меня')
	unfollow_me = BooleanField(label='отписались от меня')
	unsubscribe_me = BooleanField(label='когда отказались от моей подписки')
	comment_moderated = BooleanField(label='когда мой комментарий прошел модерацию')
	post_moderated = BooleanField(label='кода мой пост прошел модерацию')



class AddNotice_form(FlaskForm):
	'''Форма добавления уведомления.'''
	body = PageDownField(label='Текст уведомления', 
		validators=[DataRequired()])