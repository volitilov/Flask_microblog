# tests/test_user_model.py

# Тестирование модели User

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

import unittest, time
from datetime import datetime
from app import create_app, db
from app.models.user import User

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
        u = User(name='test', email='test@mail.ru', password='test')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(name='test', email='test@mail.ru', password='test')
        with self.assertRaises(AttributeError):
            u.password
  
    def test_password_verification(self):
        u = User(name='test', email='test@mail.ru', password='test')
        self.assertTrue(u.verify_password('test'))
        self.assertFalse(u.verify_password('iii'))

    def test_password_salts_are_random(self):
        u = User(name='test', email='test@mail.ru', password='test')
        u2 = User(name='test2', email='test2@mail.ru', password='test2')
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
    
    def test_timestamps(self):
        u = User(name='test', email='test@mail.ru', password='test')
        self.assertTrue(
            (datetime.utcnow() - u.date_registration).total_seconds() < 50)
        self.assertTrue(
            (datetime.utcnow() - u.last_visit).total_seconds() < 50)

    def test_ping(self):
        u = User(name='test', email='test@mail.ru', password='test')
        db.session.add(u)
        db.session.commit()
        time.sleep(2)
        last_seen_before = u.last_visit
        u.ping()
        self.assertTrue(u.last_visit > last_seen_before)

    def test_gravatar(self):
        u = User(name='test', email='volitilov@gmail.com', password='test')
        with self.app.test_request_context('/'):
            gravatar = u.gravatar()
            gravatar_256 = u.gravatar(size=256)
            gravatar_pg = u.gravatar(rating='pg')
            gravatar_retro = u.gravatar(default='retro')
        self.assertTrue('https://ru.gravatar.com/avatar/a4f45939096b109316e24e642388093b' in gravatar)
        self.assertTrue('s=256' in gravatar_256)
        self.assertTrue('r=pg' in gravatar_pg)
        self.assertTrue('d=retro' in gravatar_retro)

    # def test_follows(self):
    #     u1 = User(name='test', email='test@mail.ru', password='test')
    #     u2 = User(name='test2', email='test2@mail.ru', password='test2')
    #     db.session.add(u1)
    #     db.session.add(u2)
    #     db.session.commit()
    #     self.assertFalse(u1.is_following(u2))
    #     self.assertFalse(u1.is_followed_by(u2))
    #     timestamp_before = datetime.utcnow()
    #     u1.follow(u2)
    #     db.session.add(u1)
    #     db.session.commit()
    #     timestamp_after = datetime.utcnow()
    #     self.assertTrue(u1.is_following(u2))
    #     self.assertFalse(u1.is_followed_by(u2))
    #     self.assertTrue(u2.is_followed_by(u1))
    #     self.assertTrue(u1.followed.count() == 2)
    #     self.assertTrue(u2.followers.count() == 2)
    #     f = u1.followed.all()[-1]
    #     self.assertTrue(f.followed == u2)
    #     self.assertTrue(timestamp_before <= f.timestamp <= timestamp_after)
    #     f = u2.followers.all()[-1]
    #     self.assertTrue(f.follower == u1)
    #     u1.unfollow(u2)
    #     db.session.add(u1)
    #     db.session.commit()
    #     self.assertTrue(u1.followed.count() == 1)
    #     self.assertTrue(u2.followers.count() == 1)
    #     self.assertTrue(Follow.query.count() == 2)
    #     u2.follow(u1)
    #     db.session.add(u1)
    #     db.session.add(u2)
    #     db.session.commit()
    #     db.session.delete(u2)
    #     db.session.commit()
    #     self.assertTrue(Follow.query.count() == 1)

    def test_to_json(self):
        u = User(name='test', email='test@mail.ru', password='test')
        db.session.add(u)
        db.session.commit()
        with self.app.test_request_context('/'):
            json_user = u.to_json()
        expected_keys = ['url', 'username', 'first_name', 'last_name', 
            'about', 'location', 'date_registration', 'last_visit',
                         'posts_url', 'followed_posts_url', 'post_count']
        self.assertEqual(sorted(json_user.keys()), sorted(expected_keys))
        self.assertEqual('/api/v1.0/users/' + str(u.id), json_user['url'])