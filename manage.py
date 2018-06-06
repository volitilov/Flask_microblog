#!.venv/bin/python3

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
from dotenv import load_dotenv, find_dotenv

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# загрузка переменных необходимых для работы приложения в виртуальное
# окружение приложения
load_dotenv()

app = create_app(os.getenv('FLASK_ENV'))
migrate = Migrate(app, database)

if not app.debug:
    handler = RotatingFileHandler('tmp/loggs/warning.log', maxBytes=10000)
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
        Follow=Follow)


# flask generate_fake_data 'count'
@app.cli.command()
@click.argument('count', default=10)
def generate_fake_data(count):
    '''Генерирует фейковые данные (посты, пользователи)'''
    from app.utils import (
        generate_fake_posts, generate_fake_users, add_self_follows
    )

    generate_fake_users(count)
    add_self_follows()
    generate_fake_posts(count)



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
