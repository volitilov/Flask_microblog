# app/models/post.py

#

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from datetime import datetime

from markdown import markdown
import bleach

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


db.event.listen(Post.text, 'set', Post.on_changed_body)