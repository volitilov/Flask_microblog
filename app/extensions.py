# app/extensions.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# extension
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from flask_pagedown import PageDown

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
pagedown = PageDown()


login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login_page'
login_manager.login_message = '''Чтобы открыть данную страницу вам 
                                необходимо авторизоваться'''
