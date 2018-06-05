# instance/config.py

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

import os

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

basedir = os.path.abspath(os.path.dirname(__file__))

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', default=os.urandom(24))
    WTF_CSRF_SECRET_KEY = os.getenv('WTF_CSRF_SECRET_KEY', default=os.urandom(24))

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
    FLASKY_ADMIN = 'volitilov@gmail.com'

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'volitilov@gmail.com'
    MAIL_PASSWORD = 'Kendar6709'
    MAIL_USE_SSL = True
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

    @staticmethod
    def init_app(app): pass

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
class DevelopmentConfig(Config):
    # включение / отключение отладчика
    DEBUG = True

    # путь к файлу к базе данных.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data_dev.sqlite')


# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False

    # путь к файлу к базе данных.
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data_test.sqlite')


# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
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
class HerokuConfig(ProductionConfig):
    SSL_REDIRECT = True if os.getenv('DYNO') else False

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # обработка заголовков прокси-сервера
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

        # журналирование в поток stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig,

    'default': DevelopmentConfig
}