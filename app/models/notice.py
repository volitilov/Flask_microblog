# app/models/notice.py

#

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from datetime import datetime

from markdown2 import markdown
import bleach

from .. import db

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class Notice(db.Model):
    '''Создаёт уведомления'''
    __tablename__ = 'notice'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    body = db.Column(db.Text, nullable=False)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        '''Функция создаёт HTML-версию уведомления и сохраняет его в поле 
        body_html, обеспечивая тем самым автоматическое преобразование
        разметки Markdown в html'''
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
            'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 
            'h3', 'p', 'br']
        # target.body_html = bleach.linkify(bleach.clean(
        #     markdown(value, output_format='html'),
        #     tags=allowed_tags, strip=True))

        target.body_html = markdown(value, extras=[
            'fenced-code-blocks', 'code-friendly',
            'cuddled-lists', 'footnotes', 'header-ids', 'pyshell',
            'numbering', 'metadata', 'smarty-pants', 'spoiler', 'xml', 
            'tables', 'wiki-tables'])

    def __str__(self):
        return '<Notice - {}>'.format(self.name)


db.event.listen(Notice.body, 'set', Notice.on_changed_body)
