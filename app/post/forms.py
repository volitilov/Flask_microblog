# post/forms.py

# Файл для работы с формами

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError, HiddenField, IntegerField
from wtforms.validators import DataRequired, Length, Regexp
from flask_pagedown.fields import PageDownField

from ..models.post import Post

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class Post_form(FlaskForm):
    '''Форма добавления поста.'''
    id = IntegerField()
    title = StringField(label='Загаловок поста', validators=[DataRequired()])
    contents = PageDownField(label='Оглавление поста', validators=[DataRequired()])
    text = PageDownField(label='Текст поста', validators=[DataRequired()])
    tags = StringField(label='Теги', 
        validators=[
            DataRequired(message='Теги указывать обязательно'), 
            Length(min=1, max=24, message='Название тегов не должно превышать 24 символов'),
            Regexp(regex='^[A-Za-z][A-Za-z0-9,\s]*$', 
                message='Имена тегов должны иметь только буквы и числа')])



class AddPost_form(Post_form):
    def validate_title(self, title):
        print(self.id)
        if Post.query.filter_by(title=title.data).first():
            raise ValidationError(message='Данное название уже занято.')



class EditPost_form(Post_form):
    def validate_title(self, title):
        post = Post.query.get(self.id.data) 
        if post.title != title.data:
            if Post.query.filter_by(title=title.data).first():
                raise ValidationError(message='Данное название уже занято.')
