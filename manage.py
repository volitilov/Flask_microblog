#!.venv/bin/python3

# manage.py

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

import os, click, logging
from logging.handlers import RotatingFileHandler

from app import create_app
from app import db as database
from app.models.user import User, Follow
from app.models.user_settings import UserSettings
from app.models.role import Role
from app.models.post import Post
from app.models.tag import Tag, Rel_tag
from app.models.comment import Comment
from app.models.notice import Notice
from app.models.message import Message
from app.models.post_rating import Post_rating

from flask_migrate import Migrate, MigrateCommand
from dotenv import load_dotenv, find_dotenv

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# загрузка переменных необходимых для работы приложения в виртуальное
# окружение приложения
load_dotenv()

app = create_app(os.getenv('APP_ENV'))
migrate = Migrate(app, database)

if not app.debug:
    if not os.path.exists('tmp/loggs'):
        os.mkdir('tmp/loggs')
    handler = RotatingFileHandler('tmp/loggs/app.log', maxBytes=10240, backupCount=3)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    handler.setLevel(logging.WARNING)
    app.logger.addHandler(handler)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# команды командной строки

# flask db
@app.cli.command()
def db():
    '''Выполняет миграции базы данных'''
    return MigrateCommand


# flask shell
@app.shell_context_processor
def make_shell_context():
    '''Запускает shell со сконфигурированым контекстом'''
    return dict(app=app, db=database, User=User, Post=Post, Role=Role, 
        Follow=Follow, Comment=Comment, Notice=Notice, UserSettings=UserSettings,
        Post_rating=Post_rating, Tag=Tag, Rel_tag=Rel_tag, Message=Message)


# flask test
@app.cli.command()
def test():
    '''Запускает модульные тесты'''
    import unittest, subprocess
    tests = unittest.TestLoader().discover('tests')
    print()
    unittest.TextTestRunner(verbosity=2).run(tests)
    print()
        
    subprocess.call('rm -r data_test.sqlite', shell=True)


# flask test_cov
@app.cli.command()
def test_cov():
    import coverage, unittest, subprocess
    cov = coverage.coverage(branch=True, include='app/*')
    cov.start()

    tests = unittest.TestLoader().discover('tests')
    print()
    unittest.TextTestRunner(verbosity=2).run(tests)
    print()

    cov.stop()
    cov.save()
    print('Coverag Summary:')
    cov.report()
    basedir = os.path.abspath(os.path.dirname(__file__))
    covdir = os.path.join(basedir, 'tmp/coverage')
    cov.html_report(directory=covdir)
    print('HTML version: file://{}/index.html'.format(covdir))
    cov.erase()
        
    subprocess.call('rm -r data_test.sqlite', shell=True)


# flask profile
@app.cli.command()
@click.option('--length', default=15, 
    help='Number of functions to include in the profiler report.')
def profile(length):
    '''Запускает приложение с профилированием запросов'''

    from werkzeug.contrib.profiler import ProfilerMiddleware, MergeStream

    abs_path = os.path.abspath('')
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, 
        restrictions=[length], profile_dir=abs_path+'/tmp/profiler/')
    app.run(debug=False)



# flask deploy
@app.cli.command()
def deploy():
    '''Выполняет операции связанные с развёртыванием'''
    from flask_migrate import upgrade
    from app.utils import add_self_follows

    # обновляет базу данных до последней версии
    upgrade()

    # обновляет пользователей как читающих самих себя
    add_self_follows()



# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

if __name__ == '__main__':
    app.run()
