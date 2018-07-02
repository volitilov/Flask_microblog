# app/models/post.py

#

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from datetime import datetime

from flask import url_for, current_app
from markdown import markdown
import bleach

from app.exceptions import ValidationError
from .. import db

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class Post(db.Model):
    '''Создаёт статьи'''
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True)
    text = db.Column(db.Text)
    data_creation = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    body_html = db.Column(db.Text)
    views = db.Column(db.Integer, index=True, default=0)

    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def to_json(self):
        json_post = {
            'url': url_for('api.get_post', id=self.id, _external=True),
            'title': self.title,
            'body': self.text,
            'body_html': self.body_html,
            'timestamp': self.data_creation,
            'author': url_for('api.get_user', id=self.author_id, _external=True),
            'comments': url_for('api.get_postComments', id=self.id, _external=True),
            'comment_count': self.comments.count()
        }
        return json_post


    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        '''Функция создаёт HTML-версию поста и сохраняет её в поле 
        body_html, обеспечивая тем самым автоматическое преобразование
        разметки Markdown в html'''
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
            'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 
            'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))
    

    @staticmethod
    def from_json(json_post):
        title = json_post['title']
        body = json_post['body']

        if title is None or title == '':
            raise ValidationError('post does not have a title')
        if body is None or body == '':
            raise ValidationError('post does not have a body')
        return Post(title=title, text=body)


db.event.listen(Post.text, 'set', Post.on_changed_body)