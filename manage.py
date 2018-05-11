#!/home/py/Works/VENVS/Flask/bin/python3

# manage.py

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

import os, click
from app import create_app
from app import db as DB
from app.models import User, Role, Post

from flask_migrate import Migrate, MigrateCommand

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

app = create_app(os.getenv('FLASK_CONFIG', default='default'))
migrate = Migrate(app, DB)

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


# flask db
@app.cli.command()
def db():
    '''Выполняет миграции базы данных'''
    return MigrateCommand


# flask shell
@app.shell_context_processor
def make_shell_context():
    '''Запускает shell со сконфигурированым контекстом'''
    return dict(app=app, db=DB, User=User, Post=Post, Role=Role)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

if __name__ == '__main__':
    app.run()
