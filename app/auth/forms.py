# auth/forms.py

# Файл для работы с форммами

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo
from wtforms import ValidationError

from . import User

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class Login_form(FlaskForm):
    '''Инициализирует форму для авторизации'''
    email = StringField(label='Email', validators=[
        Required(message='Это поле обязательно'), 
        Length(min=6, max=64, message='Email-адрес не должен быть меньше 6 и больше 64 символов'),
        Email(message='Введите email')])

    password = PasswordField(label='Пароль', validators=[
        Required(message='Это поле обязательно'),
        Length(min=3, max=64, message='Пароль не должен быть меньше 8 и больше 64 символов')])

    remember_me = BooleanField(label='Запомнить меня')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if not user:
            raise ValidationError('Данный email не зарегестрирован.')

        

class Registration_form(FlaskForm):
    '''Инициализирует форму для регестрации'''
    username = StringField(label='Login', validators=[
        Required(message='Это поле обязательно'), 
        Length(min=6, max=20, message='Логин не должен быть меньше 6 и больше 20 символов'),
        Regexp(regex='^[A-Za-z][A-Za-z0-9_.]*$', message='Имена пользователей должны иметь только числа, точки или символы подчеркивания')])

    email = StringField(label='Email', validators=[
        Required(message='Это поле обязательно'), 
        Email(message='Введите реальный email'), 
        Length(min=6, max=64, message='Email-адрес не должен быть меньше 6 и больше 64 символов')])

    password = PasswordField(label='Пароль', validators=[
        Required(message='Это поле обязательно'),
        Length(min=8, max=64, message='Пароль не должен быть меньше 8 и больше 64 символов')])
    
    password2 = PasswordField(label='Повторить пароль', validators=[
        Required(message='Это поле обязательно'),
        EqualTo(fieldname='password', message='Пароли должны совпадать.')])

    # recaptcha = RecaptchaField()

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Данный email уже занят.')

    def validate_username(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('Данный login уже используется.')



class PasswordResetRequest_form(FlaskForm):
    email = StringField(label='Email', validators=[
        Required(message='Это поле обязательно'), 
        Length(min=6, max=64, message='Email-адрес не должен быть меньше 6 и больше 64 символов'), 
        Email(message='По вашему это email?')])



class PasswordReset_form(FlaskForm):
    password = PasswordField(label='Новый пароль', validators=[
        Required(message='Это поле обязательно'),
        Length(min=3, max=64, message='Пароль не должен быть меньше 8 и больше 64 символов')])

    password2 = PasswordField(label='Повторите пароль', validators=[
        Required(message='Это поле обязательно'),
        EqualTo(fieldname='password', message='Пароли должны сопадать')])
