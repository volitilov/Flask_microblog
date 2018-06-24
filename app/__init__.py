# app/__init__.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import Flask
from werkzeug import SharedDataMiddleware
from config import config
from pymemcache.client import base

# extension
from flaskext.lesscss import lesscss
from .extensions import (
    db, mail, login_manager, pagedown
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    config[config_name].init_app(app)

    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    lesscss(app)

    app.add_url_rule('/uploads/<filename>', 'uploads', build_only=True)
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        '/uploads':  app.config['UPLOAD_FOLDER']
    })
    app.memory = base.Client(('localhost', 11211))

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

    from .comment import comment
    app.register_blueprint(comment)

    from .notice import notice
    app.register_blueprint(notice)

    from .api_1_0 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1.0')

    return app
