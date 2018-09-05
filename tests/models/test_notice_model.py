# test_notice_model.py

# Тестирование модели Notice

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

import unittest
from datetime import datetime
from app import create_app, db
from app.models.user import User
from app.models.notice import Notice

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class ModelNotice_test(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_create_notice(self):
        u = User(name='test', email='test@mail.ru', password='test')
        n = Notice(body='body', author=u)
        db.session.add_all([u, n])
        db.session.commit()
        n = Notice.query.filter_by(author=u).first()
        self.assertTrue(n != None)


    def test_edit_notice(self):
        u = User(name='test', email='test@mail.ru', password='test')
        n = Notice(body='body')
        db.session.add_all([u, n])
        db.session.commit()
        n = Notice.query.filter_by(body='body').first()
        self.assertTrue(n != None)
        n.author = u
        n.title = 'new_title'
        n.body = 'new_body'
        db.session.add(n)
        db.session.commit()
        n = Notice.query.filter_by(body='new_body').first()
        self.assertTrue(n != None)
        self.assertTrue(n.author == u)
        self.assertTrue(n.title == 'new_title')
        self.assertTrue(n.timestamp < datetime.utcnow())


    def test_delete_notice(self):
        n = Notice(body='body')
        db.session.add(n)
        db.session.commit()
        n = Notice.query.filter_by(body='body').first()
        self.assertTrue(n != None)
        db.session.delete(n)
        db.session.commit()
        n = Notice.query.filter_by(body='body').first()
        self.assertTrue(n == None)

