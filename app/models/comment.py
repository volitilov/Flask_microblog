# app/models/comment.py

#

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from datetime import datetime

from markdown2 import markdown
import bleach

from .. import db
from ..exceptions import ValidationError

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class Comment(db.Model):
    '''Создаёт комментарии'''
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    state = db.Column(db.String, default='moderation')

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))


    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        '''Функция создаёт HTML-версию комментария и сохраняет его в поле 
        body_html, обеспечивая тем самым автоматическое преобразование
        разметки Markdown в html'''
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
            'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 
            'h3', 'h4', 'h5', 'h6', 'p', 'img', 'br', 'table', 'tbody', 'thead', 'td', 
            'th', 'tr', 'figcaption', '```', 'iframe', 'span']

        allowed_attrs = ['href', 'rel', 'alt', 'title', 'style', 'width', 'height', 
            'src', 'target', 'id']
        allowed_style = ['color', 'width', 'height']
        allowed_protocols=['http', 'https']
        
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, extras=[
                    'fenced-code-blocks', 'code-friendly', 'break-on-newline',
                    'cuddled-lists', 'footnotes', 'header-ids', 'pyshell',
                    'numbering', 'metadata', 'smarty-pants', 'spoiler', 'xml', 
                    'tables', 'wiki-tables']),
                attributes=allowed_attrs, tags=allowed_tags, 
                styles=allowed_style, protocols=allowed_protocols, 
                strip=True))
    

    @staticmethod
    def from_json(json_comment):
        body = json_comment['body']

        if body is None or body == '':
            raise ValidationError('Comment does not have a body')
        return Comment(body=body)
    

    def to_json(self):
        json_comment = {
            'url': url_for('api.get_comment', id=self.id, _external=True),
            'body': self.body,
            'timestamp': self.timestamp,
            'author': url_for('api.get_user', id=self.author_id, _external=True),
            'post': url_for('api.get_post', id=self.post_id, _external=True)
        }
        return json_comment


db.event.listen(Comment.body, 'set', Comment.on_changed_body)
