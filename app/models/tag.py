# app/models/tag.py

#

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from .. import db

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

add_tag = db.Table('add_tag',
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'))
)


class Tag(db.Model):
    '''Инициализирует теги.'''
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(64), unique=True, index=True)

