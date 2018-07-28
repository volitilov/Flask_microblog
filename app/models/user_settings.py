# app/models/user_settings.py

#

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from .. import db

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class UserSettings(db.Model):
    '''Создаёт объект настроек'''
    __tablename__ = 'user_settings'
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(64), index=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    comments_me = db.Column(db.Boolean, default=False)
    follow_me = db.Column(db.Boolean, default=False)
    unfollow_me = db.Column(db.Boolean, default=False)
    unsubscribe_me = db.Column(db.Boolean, default=False)
    comment_moderated = db.Column(db.Boolean, default=False)
    post_moderated = db.Column(db.Boolean, default=False)
