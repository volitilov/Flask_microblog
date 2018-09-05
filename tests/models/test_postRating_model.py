# test_postRating_model.py

# Тестирование модели Post_rating

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

import unittest
from datetime import datetime
from app import create_app, db
from app.models.user import User
from app.models.post_rating import Post_rating
from app.models.post import Post

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class ModelPostRating_test(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_create_postRating(self):
        u = User(name='test', email='test@mail.ru', password='test')
        p = Post(title='title', text='text')
        p_r = Post_rating(author=u, post=p)
        db.session.add_all([u, p, p_r])
        db.session.commit()
        p_r = Post_rating.query.filter_by(author=u).first()
        self.assertTrue(p_r != None)
        

    def test_edit_postRating(self):
        u = User(name='test', email='test@mail.ru', password='test')
        p = Post(title='title', text='text')
        p_r = Post_rating(author=u)
        db.session.add_all([u, p, p_r])
        db.session.commit()

        p_r.post = p
        db.session.add(p_r)
        db.session.commit()
        p_r = Post_rating.query.filter_by(post=p).first()
        self.assertTrue(p_r != None)


    def test_delete_postRating(self):
        u = User(name='test', email='test@mail.ru', password='test')
        p_r = Post_rating(author=u)
        db.session.add_all([u, p_r])
        db.session.commit()
        p_r = Post_rating.query.filter_by(author=u).first()
        self.assertTrue(p_r != None)
        db.session.delete(p_r)
        db.session.commit()
        p_r = Post_rating.query.filter_by(author=u).first()
        self.assertTrue(p_r == None)

