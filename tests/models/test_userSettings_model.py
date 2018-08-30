# test_userSettings_model.py

# Тестирование модели UserSettings

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

import unittest
from datetime import datetime
from app import create_app, db
from app.models.user import User
from app.models.user_settings import UserSettings

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class ModelUserSettings_test(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_create_userSettings(self):
        u = User(name='test', email='test@mail.ru', password='test')
        u_s = UserSettings(state='test', profile=u)
        db.session.add_all([u, u_s])
        db.session.commit()
        u_s = UserSettings.query.filter_by(profile=u).first()
        self.assertTrue(u_s != None)


    def test_edit_userSettings(self):
        u = User(name='test', email='test@mail.ru', password='test')
        u_s = UserSettings(state='test', profile=u)
        db.session.add_all([u, u_s])
        db.session.commit()
        u_s = UserSettings.query.filter_by(profile=u).first()
        self.assertTrue(u_s.comments_me == False)
        u_s.comments_me = True
        self.assertTrue(u_s.follow_me == False)
        u_s.follow_me = True
        self.assertTrue(u_s.unfollow_me == False)
        u_s.unfollow_me = True
        self.assertTrue(u_s.unsubscribe_me == False)
        u_s.unsubscribe_me = True
        self.assertTrue(u_s.comment_moderated == False)
        u_s.comment_moderated = True
        self.assertTrue(u_s.post_moderated == False)
        u_s.post_moderated = True
        db.session.add(u_s)
        db.session.commit()
        u_s = UserSettings.query.filter_by(profile=u).first()
        self.assertTrue(u_s.comments_me != False)
        self.assertTrue(u_s.follow_me != False)
        self.assertTrue(u_s.unfollow_me != False)
        self.assertTrue(u_s.unsubscribe_me != False)
        self.assertTrue(u_s.comment_moderated != False)
        self.assertTrue(u_s.post_moderated != False)



    def test_delete_userSettings(self):
        u = User(name='test', email='test@mail.ru', password='test')
        u_s = UserSettings(state='test', profile=u)
        db.session.add_all([u, u_s])
        db.session.commit()
        u_s = UserSettings.query.filter_by(profile=u).first()
        self.assertTrue(u_s != None)
        db.session.delete(u_s)
        db.session.commit()
        u_s = UserSettings.query.filter_by(profile=u).first()
        self.assertTrue(u_s == None)

