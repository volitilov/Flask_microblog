#!/home/x/Works/.VENVS/BLOG/bin/python3.5

# manage.py

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

import os, click

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

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

if __name__ == '__main__':
    app.run()
