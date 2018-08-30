# test_search_model.py

# Тестирование модели SearchableMixin

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

import unittest
from datetime import datetime
from app import create_app, db
from app.models.post import Post

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class ModelSearchableMixin_test(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_search_post(self):
        p = Post(title='title', text='text')
        db.session.add(p)
        db.session.commit()
        posts, _ = Post.search('text', 1, 5)
        self.assertTrue(posts.all()[0] == p)
        self.assertTrue(posts.count() == 1)
        posts, _ = Post.search('title', 1, 5)
        self.assertTrue(posts.all()[0] == p)
        self.assertTrue(posts.count() == 1)
        
