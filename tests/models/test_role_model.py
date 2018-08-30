# test_role_model.py

# Тестирование модели Role

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

import unittest
from datetime import datetime
from app import create_app, db
from app.models.user import User
from app.models.role import Role

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class ModelRole_test(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_create_role(self):
        r = Role(name='test')
        db.session.add(r)
        db.session.commit()
        r = Role.query.filter_by(name='test').first()
        self.assertTrue(r != None)
        

    def test_edit_role(self):
        r = Role(name='test')
        u = User(name='test', email='test@mail.ru', password='test')
        u.role = r
        db.session.add_all([u, r])
        db.session.commit()
        r = Role.query.filter_by(name='test').first()
        u = User.query.filter_by(name='test').first()
        self.assertTrue(u.role == r)
        self.assertTrue(r.users[0] == u)


    def test_delete_role(self):
        r = Role(name='test')
        db.session.add(r)
        db.session.commit()
        r = Role.query.filter_by(name='test').first()
        self.assertTrue(r != None)
        db.session.delete(r)
        db.session.commit()
        r = Role.query.filter_by(name='test').first()
        self.assertTrue(r == None)
