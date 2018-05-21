# app/models/model_post.py

#

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from datetime import datetime

from .. import db
from .user import User

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class Post(db.Model):
    '''Создаёт статьи'''
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True)
    text = db.Column(db.Text)
    data_creation = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py as forgery

        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            p = Post(title=forgery.lorem_ipsum.title(),
                    text=forgery.lorem_ipsum.sentences(randint(1, 4)),
                    author=u,
                    data_creation=forgery.date.date(True))
            db.session.add(p)
            db.session.commit()

