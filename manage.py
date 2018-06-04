#!/home/x/Works/.VENVS/BLOG/bin/python3.5

# manage.py

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

import os, click, logging
from logging.handlers import RotatingFileHandler

from app import create_app
from app import db as database
from app.models.user import User, Follow
from app.models.role import Role
from app.models.post import Post

from flask_migrate import Migrate, MigrateCommand
from dotenv import load_dotenv, find_dotenv, dotenv_values

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

load_dotenv(find_dotenv('.env'))

app = create_app(os.getenv('FLASK_CONFIG'))
migrate = Migrate(app, database)

if not app.debug:
    handler = RotatingFileHandler('tmp/loggs/wrning.log', maxBytes=10000)
    handler.setLevel(logging.WARNING)
    app.logger.addHandler(handler)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# команды командной строки

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
        Follow=Follow)


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
