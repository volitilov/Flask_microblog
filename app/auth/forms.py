# auth/forms.py

#

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from wtforms import ValidationError

from ..models.user import User

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class Login_form(FlaskForm):
    email = StringField(label='Email', 
        validators=[DataRequired(message='Это поле обязательно'), Email(), Length(1, 64)])
    password = PasswordField(label='Пароль', 
        validators=[DataRequired(message='Это поле обязательно')])
    remember_me = BooleanField(label='Запомнить меня')


class Registration_form(FlaskForm):
    username = StringField(label='Login', 
        validators=[DataRequired(message='Это поле обязательно'), Length(1, 64),
                                  Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 
        'Имена пользователей должны иметь только числа, точки или символы подчеркивания')])

    email = StringField(label='Email', 
        validators=[DataRequired(message='Это поле обязательно'), Email(), Length(1, 64)])
    password = PasswordField(label='Пароль', 
        validators=[DataRequired(message='Это поле обязательно'), 
                        EqualTo('password2', message='Пароли должны совпадать.')])
    password2 = PasswordField(label='Повторить пароль', 
        validators=[DataRequired(message='Это поле обязательно')])
    recaptcha = RecaptchaField()

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email уже занят.')

    def validate_username(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('Username уже используется.')


class PasswordResetRequest_form(FlaskForm):
    email = StringField(label='Email', 
        validators=[DataRequired(message='Это поле обязательно'), Length(1, 64), Email()])


class PasswordReset_form(FlaskForm):
    password = PasswordField(label='Новый пароль', validators=[
        DataRequired(message='Это поле обязательно'), 
        EqualTo('password2', message='Пароли должны сопадать')])
    password2 = PasswordField(label='Повторите пароль', 
        validators=[DataRequired(message='Это поле обязательно')])
