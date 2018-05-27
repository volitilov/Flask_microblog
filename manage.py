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

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

app = create_app(os.getenv('FLASK_CONFIG', default='default'))
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
