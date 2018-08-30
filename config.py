# instance/config.py

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

import os
from dotenv import load_dotenv

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    WTF_CSRF_SECRET_KEY = os.getenv('WTF_CSRF_SECRET_KEY')

    RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY')
    RECAPTCHA_DATA_ATTRS = {'theme': 'light'}

    ELASTICSEARCH_URL = os.getenv('ELASTICSEARCH_URL')

    # включение / отключение CSRF
    WTF_CSRF_ENABLED = True

    # задаёт кол-во элементов на станице
    APP_POSTS_PER_PAGE = 5
    APP_FOLLOWERS_PER_PAGE = 10
    APP_NOTICE_PER_PAGE = 5

    FLASK_COVERAGE = True

    # включает запись информации о запросах
    SQLALCHEMY_RECORD_QUERIES = True
    # устанавливает порог выше которого запросы считаются медленными
    FLASKY_SLOW_DB_QUERY_TIME = 0.5

    # папка, где храняться файлы SQLAlchemy-migrate
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    # отслеживет изменение объектов и испускает сигналы
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # путь загрузки файлов
    UPLOAD_FOLDER = basedir + '/uploads'
    # разрешонные расширения для изображений
    ALLOWED_EXTENSIONS = set(['.png', '.jpg', '.jpeg', '.gif', '.svg'])

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    APP_MAIL_SENDER = 'Admin volitilov@gmail.com'
    APP_MAIL_SUBJECT_PREFIX = '[ voliTilov ] '
    APP_ADMIN = os.getenv('APP_ADMIN')
    APP_MODERATOR = os.getenv('APP_MODERATOR')

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_SSL = True
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

    VK_APP_SECRET_KEY = os.getenv('VK_APP_SECRET_KEY')
    VK_APP_ID = os.getenv('VK_APP_ID')
    VK_VERSION = '5.52'
    VK_AUTHORIZATION_URL = 'https://oauth.vk.com/authorize'

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
            fromaddr=cls.APP_MAIL_SENDER,
            toaddrs=[cls.APP_ADMIN],
            subject=cls.APP_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler) 


# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False

    # путь к файлу к базе данных.
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 
        'data_test.sqlite')

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}