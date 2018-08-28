# app/models/post.py

#

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from datetime import datetime
from urllib.parse import urlparse

from flask import url_for, current_app
from markdown2 import markdown
import bleach
from bleach.linkifier import Linker

from app.exceptions import ValidationError
from .tag import Rel_tag
from .search import SearchableMixin
from .. import db

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class Post(SearchableMixin, db.Model):
    '''Создаёт статьи'''
    __tablename__ = 'posts'
    __searchable__ = ['title', 'text']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True)
    table_of_contents = db.Column(db.Text)
    text = db.Column(db.Text)
    data_creation = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    body_html = db.Column(db.Text)
    t_contents_html = db.Column(db.Text)
    views = db.Column(db.Integer, index=True, default=0)
    rating = db.Column(db.Integer, index=True, default=0)
    state = db.Column(db.String, default='develop')

    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    ratings = db.relationship('Post_rating', backref='post', lazy='dynamic')
    tags = db.relationship('Rel_tag', foreign_keys=[Rel_tag.tag_id],
            backref=db.backref('post', lazy='joined'),
            lazy='dynamic', cascade='all, delete-orphan')

    def to_json(self):
        return {
            'id': self.id,
            'url': url_for('api.get_post', id=self.id, _external=True),
            'title': self.title,
            't_contents': self.t_contents_html,
            'body': self.body_html,
            'timestamp': self.data_creation,
            'views': self.views,
            'rating': self.rating,
            'author': url_for('api.get_user', id=self.author_id, _external=True),
            'comments': url_for('api.get_postComments', id=self.id, _external=True),
            'comment_count': self.comments.count()
        }


    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        '''Функция создаёт HTML-версию поста и сохраняет её в поле 
        body_html, обеспечивая тем самым автоматическое преобразование
        разметки Markdown в html'''
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
            'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 
            'h3', 'h4', 'h5', 'h6', 'p', 'img', 'br', 'table', 'tbody', 
            'tfoot', 'thead', 'td', 
            'th', 'tr', '```', 'iframe', 'span', 'font']

        allowed_attrs = ['href', 'rel', 'alt', 'title', 'style', 'width', 'height', 
            'src', 'target', 'id', 'color']
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
    def on_changed_table_of_contents(target, value, oldvalue, initiator):
        '''Функция создаёт HTML-версию оглавления и сохраняет её в том
        же поле'''
        allowed_tags = ['a', 'li', 'ol', 'ul']

        allowed_attrs = ['href', 'rel', 'alt', 'title', 'id']
        allowed_protocols=['http', 'https']

        def change_url(attrs, new=False):
            p = urlparse(attrs[(None, u'href')])
            if p.netloc not in ['blacklist.com', 'other-domain.com']:
                attrs[(None, u'rel')] = u'nofollow'
                attrs[(None, u'href')] = u'/posts/{}{}'.format(target.id, attrs[(None, u'href')])
            else:
                attrs.pop((None, u'target'), None)
            return attrs

        linker = Linker(callbacks=[change_url])
        
        target.t_contents_html = linker.linkify(bleach.clean(
            markdown(value, extras=['break-on-newline',
                    'cuddled-lists', 'footnotes']),
                attributes=allowed_attrs, tags=allowed_tags, 
                protocols=allowed_protocols, strip=True))
    

    @staticmethod
    def from_json(json_post):
        title = json_post.get('title')
        table_of_contents = json_post.get('table_of_contents')
        body = json_post.get('body')
        tags = json_post.get('tags')

        if Post.query.filter_by(title=title).first():
            raise ValidationError('Данный заголовок уже занят.')

        for key, value in locals().items():
            if value is None or value == '':
                raise ValidationError(' [ {} ] - является обязательным.'.format(key))

        return Post(title=title, text=body, state='moderation',
                table_of_contents=table_of_contents)


db.event.listen(Post.text, 'set', Post.on_changed_body)
db.event.listen(Post.table_of_contents, 'set', Post.on_changed_table_of_contents)
db.event.listen(db.session, 'before_commit', Post.before_commit)
db.event.listen(db.session, 'after_commit', Post.after_commit)
