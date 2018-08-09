# moderator/utils.py

# утилиты необходимые для работы данного пакета

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from functools import wraps

from flask import redirect, url_for, flash

from flask_login import current_user, login_required


# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

def is_moderator(func):
    '''Обёртка для проверки пользователя на авторизацию и является ли
    текущий пользователь модератором.'''
    @wraps(func)
    @login_required
    def wrap(*args, **kwargs):
        if not current_user.is_moderator():
            flash(category='warn', message='Тебе туда нельзя')
            return redirect(url_for('main.home_page'))
        else:
            return func(*args, **kwargs)
    return wrap
