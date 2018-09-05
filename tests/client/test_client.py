# tests/test_client.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

import unittest
import re
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
        self.assertTrue(b'freelance' in response.data)


    def test_register_and_login(self):
        # регистрация новой учётной записи
        response = self.client.post('/registration_form_request', data={
            'email': 'test@mail.ru',
            'username': 'deeplogger2',
            'password': '12345678',
            'password2': '12345678'
        })
        self.assertTrue(response.status_code, 302)

        # аутентификация с новой учетной записью
        response = self.client.post('/login_form_request', data={
            'email': 'test@mail.ru',
            'password': '12345678'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(re.search(b'next_url', response.data))
        
        # выход
        response = self.client.get('/...logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(u'Вы успешно вышли' in response.data.decode('utf-8'))