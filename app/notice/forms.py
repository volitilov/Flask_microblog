# notice/forms.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired
from flask_pagedown.fields import PageDownField

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class AddNotice_form(FlaskForm):
	'''Форма добавления уведомления.'''
	body = PageDownField(label='Текст уведомления', 
		validators=[DataRequired()])


class SettingsNotice_form(FlaskForm):
	'''Форма настроек уведомлений.'''
	comments_me = BooleanField(label='оставили комментарий к посту')
	follow_me = BooleanField(label='подписались на меня')
	unfollow_me = BooleanField(label='отписались от меня')
	unsubscribe_me = BooleanField(label='когда отказались от моей подписки')
	comment_moderated = BooleanField(label='когда мой комментарий прошел модерацию')
	post_moderated = BooleanField(label='кода мой пост прошел модерацию')
