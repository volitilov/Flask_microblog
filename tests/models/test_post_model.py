# test_post_model.py

# Тестирование модели Post

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

import unittest, time
from datetime import datetime
from app import create_app, db
from app.models.user import User
from app.models.comment import Comment
from app.models.post import Post

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class ModelPost_test(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_create_post(self):
        u = User(name='test', email='test@mail.ru', password='test')
        p = Post(title='title', text='text', author=u)
        db.session.add_all([u, p])
        db.session.commit()
        p = Post.query.filter_by(title='title').first()
        self.assertTrue(p != None)
        self.assertTrue(p.author == u)


    def test_edit_post(self):
        u = User(name='test', email='test@mail.ru', password='test')
        p = Post(title='title', text='text')
        db.session.add(p)
        db.session.commit()
        p = Post.query.filter_by(title='title').first()
        p.text = 'new_text'
        p.title = 'new_title'
        p.author = u
        p.table_of_contents = 'table_of_contents'
        p.views += 1
        p.state = 'test'
        p.rating += 1
        db.session.add(p)
        db.session.commit()
        p = Post.query.filter_by(text='new_text').first()
        self.assertTrue(p != None)
        self.assertFalse(p.title == 'title')
        self.assertTrue(p.author == u)
        self.assertTrue(p.table_of_contents == 'table_of_contents')
        self.assertFalse(p.views < 1)
        self.assertFalse(p.rating < 1)
        self.assertFalse(p.state == 'develop')
        self.assertTrue(p.data_creation < datetime.utcnow())


    def test_delete_post(self):
        p = Post(title='title', text='text')
        db.session.add(p)
        db.session.commit()
        p = Post.query.filter_by(title='title').first()
        self.assertTrue(p != None)
        db.session.delete(p)
        db.session.commit()
        p = Post.query.filter_by(title='title').first()
        self.assertTrue(p == None)


    def test_addComment_post(self):
        p = Post(title='title', text='text')
        c = Comment(body='body', post=p)
        db.session.add_all([p, c])
        db.session.commit()
        p = Post.query.filter_by(title='title').first()
        c = Comment.query.filter_by(post=p).first()
        self.assertTrue(c != None)

    
    def test_to_json(self):
        u = User(name='test', email='test@mail.ru', password='test')
        p = Post(title='title', text='text', author=u)
        db.session.add_all([p, u])
        db.session.commit()
        with self.app.test_request_context('/'):
            json_post = p.to_json()
        expected_keys = ['url', 'title', 't_contents', 'body', 'timestamp',
            'views', 'rating', 'author', 'comments', 'comment_count']
        self.assertEqual(sorted(json_post.keys()), sorted(expected_keys))
        self.assertEqual('/api/v1.0/posts/' + str(p.id), json_post['url']) 
