# main/forms.py

# Файл для работы с формами

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import request
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class Search_form(FlaskForm):
    q = StringField(label='Поиск', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(Search_form, self).__init__(*args, **kwargs)
