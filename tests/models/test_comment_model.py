# test_comment_model.py

# Тестирование модели Comment

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

import unittest, time
from datetime import datetime
from app import create_app, db
from app.models.user import User
from app.models.comment import Comment
from app.models.post import Post

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class ModelComment_test(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_create_comment(self):
        c = Comment(body='body')
        db.session.add(c)
        db.session.commit()
        c = Comment.query.filter_by(body='body').first()
        self.assertTrue(c != None)


    def test_edit_comment(self):
        u = User(name='test', email='test@mail.ru', password='test')
        p = Post(title='title', text='text')
        c = Comment(body='body', author=u, post=p)
        db.session.add_all([c, u, p])
        db.session.commit()
        c = Comment.query.filter_by(body='body').first()
        c.title = 'new_title'
        c.body = 'new_message'
        c.state = 'test'
        db.session.add(c)
        db.session.commit()
        c = Comment.query.filter_by(body='new_message').first()
        self.assertFalse(c == None)
        self.assertTrue(c.title != 'title')
        self.assertTrue(c.author == u)
        self.assertTrue(c.post == p)
        self.assertTrue(c.timestamp < datetime.utcnow())
        self.assertFalse(c.state == 'develop')


    def test_delete_comment(self):
        c = Comment(body='body')
        db.session.add(c)
        db.session.commit()
        c = Comment.query.filter_by(body='body').first()
        db.session.delete(c)
        db.session.commit()
        c = Comment.query.filter_by(body='body').first()
        self.assertTrue(c == None)


    def test_to_json(self):
        u = User(name='test', email='test@mail.ru', password='test')
        p = Post(title='title', text='text')
        c = Comment(body='body', author=u, post=p)
        db.session.add_all([c, u, p])
        db.session.commit()
        with self.app.test_request_context('/'):
            json_comment = c.to_json()
        expected_keys = ['url', 'body', 'timestamp', 'author', 'post']
        self.assertEqual(sorted(json_comment.keys()), sorted(expected_keys))
        self.assertEqual('/api/v1.0/comments/' + str(c.id), json_comment['url']) 

