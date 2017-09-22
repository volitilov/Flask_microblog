import os


basedir = os.path.abspath(os.path.dirname(__file__))


# путь к файлу к базе данных.
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
# папка, где храняться файлы SQLAlchemy-migrate
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
# отслеживет изменение объектов и испускает сигналы
SQLALCHEMY_TRACK_MODIFICATIONS = False


# включение / отключение CSRF
CSRF_ENABLED = True

SECRET_KEY = os.urandom(24)

  
OPENID_PROVIDERS = [
  { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
  { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
  { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
  { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
  { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]
