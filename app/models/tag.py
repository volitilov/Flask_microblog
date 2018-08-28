# app/models/tag.py

#

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from datetime import datetime

from .. import db

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class Rel_tag(db.Model):
    __tablename__ = 'rel_tag'
    tag_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())



class Tag(db.Model):
    '''Инициализирует теги.'''
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(64), unique=True, index=True)

    posts = db.relationship('Rel_tag', foreign_keys=[Rel_tag.post_id],
            backref=db.backref('tag', lazy='joined'),
            lazy='dynamic', cascade='all, delete-orphan')

