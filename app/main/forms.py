# main/forms.py

# Файл для работы с формами

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import request
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms import StringField, TextAreaField

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class Search_form(FlaskForm):
    q = StringField(label='Поиск', validators=[
            DataRequired(message='Как можно найти ничто?')])



class Support_form(FlaskForm):
    title = StringField(label='Заголовок', validators=[
        Length(min=10, max=100, message='Зоголовок не может быть меньше 10 и больше 100 символов')
    ])
    body = TextAreaField(label='Текст сообщения', validators=[
        Length(min=30, max=1000, message='Текст сообщения не может быть меньше 30 и больше 1000 символов')
    ])
