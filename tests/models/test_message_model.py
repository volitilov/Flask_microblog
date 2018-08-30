# test_message_model.py

# Тестирование модели Message

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

import unittest
from datetime import datetime
from app import create_app, db
from app.models.user import User
from app.models.message import Message

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class ModelMessage_test(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_create_message(self):
        u1 = User(name='user1', email='user1@mail.ru', password='user1')
        u2 = User(name='user2', email='user2@mail.ru', password='user2')
        m = Message(body='body', author=u1, recipient=u2)
        db.session.add_all([u1, u2, m])
        db.session.commit()
        m = Message.query.filter_by(body='body').first()
        self.assertTrue(m != None)
        


    def test_edit_message(self):
        u1 = User(name='user1', email='user1@mail.ru', password='user1')
        u2 = User(name='user2', email='user2@mail.ru', password='user2')
        m = Message(body='body')
        db.session.add_all([u1, u2, m])
        db.session.commit()
        m = Message.query.filter_by(body='body').first()
        m.author = u1
        m.recipient = u2
        m.title = 'new_title'
        db.session.add(m)
        db.session.commit()
        m = Message.query.filter_by(title='new_title').first()
        self.assertTrue(m != None)
        self.assertTrue(m.author == u1)
        self.assertTrue(m.author != u2)
        self.assertTrue(m.recipient == u2)
        self.assertTrue(m.recipient != u1)
        self.assertTrue(m.timestamp < datetime.utcnow())



    def test_delete_message(self):
        m = Message(body='body')
        db.session.add(m)
        db.session.commit()
        m = Message.query.filter_by(body='body').first()
        self.assertTrue(m != None)
        db.session.delete(m)
        db.session.commit()
        m = Message.query.filter_by(body='body').first()
        self.assertTrue(m == None)

