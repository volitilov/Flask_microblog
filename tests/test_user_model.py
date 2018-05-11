# test_user_model.py

# Тестирование модели User

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

import unittest, time
from app import create_app, db
from app.models import User

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class UserModelTestCash(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = User(password='test')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='test')
        with self.assertRaises(AttributeError):
            u.password
  
    def test_password_verification(self):
        u = User(password='test')
        self.assertTrue(u.verify_password('test'))
        self.assertFalse(u.verify_password('iii'))

    def test_password_salts_are_random(self):
        u = User(password='test')
        u2 = User(password='xxx')
        self.assertTrue(u.password_hash != u2.password_hash)


    def test_valid_confirmation_token(self):
        u = User(name='test', email='test@mail.ru', password='test')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token()
        self.assertTrue(u.confirm(token))

    def test_invalid_confirmation_token(self):
        u = User(name='test', email='test@mail.ru', password='test')
        u2 = User(name='test2', email='test2@mail.ru', password='test2')
        db.session.add(u)
        db.session.add(u2)
        db.session.commit()
        token = u.generate_confirmation_token()
        self.assertFalse(u2.confirm(token))

    def test_expired_confirmation_token(self):
        u = User(name='test', email='test@mail.ru', password='test')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token(1)
        time.sleep(2)
        self.assertFalse(u.confirm(token))

    def test_valid_reset_token(self):
        u = User(name='test', email='test@mail.ru', password='test')
        db.session.add(u)
        db.session.commit()
        token = u.generate_resetPassword_token()
        self.assertTrue(User.reset_password(token, 'qwe'))
        self.assertTrue(u.verify_password('qwe'))

    def test_invalid_reset_token(self):
        u = User(name='test', email='test@mail.ru', password='test')
        db.session.add(u)
        db.session.commit()
        token = u.generate_resetPassword_token()
        self.assertFalse(User.reset_password(token+'x', 'qwe'))
        self.assertTrue(u.verify_password('test'))

    def test_valid_email_change_token(self):
        u = User(name='test', email='test@mail.ru', password='test')
        db.session.add(u)
        db.session.commit()
        token = u.generate_changeEmail_token('susan@example.org')
        self.assertTrue(u.change_email(token))
        self.assertTrue(u.email == 'susan@example.org')

    def test_invalid_email_change_token(self):
        u = User(name='test', email='test@mail.ru', password='test')
        u2 = User(name='test2', email='test2@mail.ru', password='test2')
        db.session.add(u)
        db.session.add(u2)
        db.session.commit()
        token = u.generate_changeEmail_token('david@example.net')
        self.assertFalse(u2.change_email(token))
        self.assertTrue(u2.email == 'test2@mail.ru')

    def test_duplicate_email_change_token(self):
        u = User(name='test', email='test@mail.ru', password='test')
        u2 = User(name='test2', email='test2@mail.ru', password='test2')
        db.session.add(u)
        db.session.add(u2)
        db.session.commit()
        token = u2.generate_changeEmail_token('test@mail.ru')
        self.assertFalse(u2.change_email(token))
        self.assertTrue(u2.email == 'test2@mail.ru')

    def test_is_admin(self):
        admin = User(name='admin', email='volitilov@gmail.com', password='qwe')
        no_admin = User(name='no_admin', email='ex@mail.ru', password='ewq')
        db.session.add_all([admin, no_admin])
        db.session.commit()
        self.assertTrue(admin.is_admin())
        self.assertFalse(no_admin.is_admin())
