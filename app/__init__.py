# app/__init__.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import Flask
from config import config

# extension
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail
from flask_login import LoginManager
from flaskext.lesscss import lesscss
from flask_wtf.csrf import CSRFProtect

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

db = SQLAlchemy()
toolbar = DebugToolbarExtension()
mail = Mail()
login_manager = LoginManager()
csrf = CSRFProtect()

login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login_page'
login_manager.login_message = '''Чтобы открыть данную страницу вам 
                                необходимо авторизоваться'''


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    config[config_name].init_app(app)
    db.init_app(app)
    # toolbar.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    lesscss(app)

    from .main import main
    app.register_blueprint(main)

    from .auth import auth
    app.register_blueprint(auth)

    from .admin import admin
    app.register_blueprint(admin)

    from .user import user
    app.register_blueprint(user)

    from .post import post
    app.register_blueprint(post)

    return app
