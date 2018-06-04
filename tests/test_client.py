# tests/test_client.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

import unittest

from app import create_app, db
from app.models.user import User

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Stranger' in response.data)


    def test_register(self):
        # регистрация новой учётной записи
        response = self.client.post('/auth/register', data={
            'email': 'test@mail.ru',
            'username': 'Bob',
            'password': 'test',
            'password2': 'test'
        })
        self.assertTrue(response.status_code, 302)


    # def test_login(self):
    #     # аутентификация с новой учетной записью
    #     response = self.client.post('/auth/login', data={
    #         'email': 'test@mail.ru',
    #         'password': 'test',
    #         'remember_me': 'True'
    #     }, follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(re.search(b'Hello,\s+Bob!', response.data))
    #     self.assertTrue(
    #         b'You have not confirmed your account yet.' in response.data)
        
    #     # отправка маркера подтверждения
    #     user = User.query.filter_by(email='test@mail.ru').first()
    #     token = user.generate_confirmation_token()
    #     response = self.client.get('/auth/confirm/{}'.format(token), 
    #         follow_redirects=True)
    #     user.confirm(token)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(
    #         b'You have confirmed your account' in response.data)


    # def test_logout(self):
    #     # выход
    #     response = self.client.get('/auth/logout', follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(b'You have been logged out' in response.data)
