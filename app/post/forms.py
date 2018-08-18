# post/forms.py

# Файл для работы с формами

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask_wtf import FlaskForm
from wtforms import (
    StringField, ValidationError, HiddenField, IntegerField, 
    TextAreaField)
from wtforms.validators import DataRequired, Length, Regexp

from ..models.post import Post

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class Post_form(FlaskForm):
    '''Форма добавления поста.'''
    id = IntegerField()
    title = StringField(label='Загаловок поста', validators=[
        Length(min=10, max=200, message='Заглавие не может быть меньше 10, больше 200 символов.')])
    contents = TextAreaField(label='Оглавление поста', validators=[
        Length(min=10, max=1000, message='Оглавление не может быть меньше 10, больше 1000 символов.')])
    text = TextAreaField(label='Текст поста', validators=[
        Length(min=200, max=20000, message='Пост не может быть меньше 200, больше 20000 символов.')])
    tags = StringField(label='Теги', 
        validators=[
            DataRequired(message='Теги указывать обязательно'), 
            Length(max=100, message='Сумма названий тегов не должна превышать 100 символов'),
            Regexp(regex='^[A-Za-z][A-Za-z0-9,\s]*$', 
                message='Имена тегов должны иметь только буквы и числа')])



class AddPost_form(Post_form):
    def validate_title(self, title):
        if Post.query.filter_by(title=title.data).first():
            raise ValidationError(message='Данное название уже занято.')



class EditPost_form(Post_form):
    def validate_title(self, title):
        post = Post.query.get(self.id.data) 
        if post.title != title.data:
            if Post.query.filter_by(title=title.data).first():
                raise ValidationError(message='Данное название уже занято.')
