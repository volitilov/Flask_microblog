# app/models/post_rating.py

#

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from .. import db

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class Post_rating(db.Model):
    '''Инициализирует рейтинг к посту'''
    __tablename__ = 'post_reiting'
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, default=0)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
