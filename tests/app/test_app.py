# tests/test_basics.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

import unittest
from flask import current_app
from app import create_app, db

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class BasicsTestCase(unittest.TestCase):
    # выполняется до каждого теста метод setUp пытается создать окружение 
    # для теста, близко напоминающее действующее приложение. Сначала он 
    # создаёт экземпляр приложения, настроенный для тестирования, и 
    # активирует его контекст. Это шаг гарантирует current_app для теста. 
    # Затем он созаёт новую базу данных, которая может использоваться 
    # тестами.
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()


    # выполняется после каждого теста tearDown удаляет базу даных и 
    # контекст после тестирования
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()



    # проверяет наличие экземпляра приложения
    def test_app_exist(self):
        self.assertFalse(current_app is None)


    # убеждается, что приложение выполняется с настройками 
    # для тестирования
    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])