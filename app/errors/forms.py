# errors/forms.py

# Файл для работы с формами

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class Search_form(FlaskForm):
    q = StringField(label='', validators=[
            DataRequired(message='Как можно найти ничто?')])

