# instance/config.py

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

import os
from dotenv import load_dotenv, find_dotenv

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    WTF_CSRF_SECRET_KEY = os.getenv('WTF_CSRF_SECRET_KEY')

    # включение / отключение CSRF
    WTF_CSRF_ENABLED = True

    # задаёт кол-во элементов на станице
    FLASKY_POSTS_PER_PAGE = 5
    FLASKY_FOLLOWERS_PER_PAGE = 10

    # включает запись информации о запросах
    SQLALCHEMY_RECORD_QUERIES = True
    # устанавливает порог выше которого запросы считаются медленными
    FLASKY_SLOW_DB_QUERY_TIME = 0.5

    SSL_REDIRECT = False

    # папка, где храняться файлы SQLAlchemy-migrate
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    # отслеживет изменение объектов и испускает сигналы
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    FLASKY_MAIL_SENDER = 'Admin volitilov@gmail.com'
    FLASKY_MAIL_SUBJECT_PREFIX = '[ voliTilov ] '
    FLASKY_ADMIN = os.getenv('FLASK_ADMIN')

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_SSL = True
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

    @staticmethod
    def init_app(app): pass

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
class DevelopmentConfig(Config):
    # включение / отключение отладчика
    FLASK_DEBUG = True

    # путь к файлу к базе данных.
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL')


# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # отправляет администратору письма с сообщениями об ошибках
        import logging
        from logging.handlers import SMTPHandler

        credentials = None
        secure = None

        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.FLASKY_MAIL_SENDER,
            toaddrs=[cls.FLASKY_ADMIN],
            subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler) 



# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}