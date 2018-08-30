# test_tag_model.py

# Тестирование модели Tag

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

import unittest
from datetime import datetime
from app import create_app, db
from app.models.user import User
from app.models.post import Post
from app.models.tag import Tag, Rel_tag

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class ModelTag_test(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_create_tag(self):
        p = Post(title='title')
        t = Tag(name='tag')
        r_t = Rel_tag(post=p, tag=t)
        db.session.add_all([p, t, r_t])
        db.session.commit()
        t = Tag.query.filter_by(name='tag').first()
        self.assertTrue(t != None)
        r_t = t.posts[0]
        self.assertTrue(r_t.timestamp < datetime.utcnow())
        self.assertTrue(r_t.post == p)


    def test_delete_tag(self):
        p = Post(title='title')
        t = Tag(name='tag')
        r_t = Rel_tag(post=p, tag=t)
        db.session.add_all([p, t, r_t])
        db.session.commit()
        t = Tag.query.filter_by(name='tag').first()
        self.assertTrue(t != None)
        r_t = Rel_tag.query.filter_by(tag=t).first()
        self.assertTrue(r_t != None)
        db.session.delete(t)
        db.session.delete(r_t)
        db.session.commit()
        t = Tag.query.filter_by(name='tag').first()
        self.assertTrue(t == None)
        r_t = Rel_tag.query.filter_by(tag=t).first()
        self.assertTrue(r_t == None)


