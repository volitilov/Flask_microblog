# app/utils.py

#

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from random import randint
from functools import wraps

from flask import (
	make_response, render_template, request, current_app, url_for,
	redirect, flash, abort
)
from sqlalchemy.exc import IntegrityError
from flask_login import current_user, login_required

from . import db
from .models.post import Post
from .models.user import User

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

def create_response(template, data):
	'''Делает обёртку для объекта ответа.'''
	resp = make_response(render_template(template, data=data))
	resp.delete_cookie('next')
	resp.set_cookie(key='current_page', value=request.full_path)
	if request.args.get('next') is not None: 
		resp.set_cookie(key='next', value=request.args.get('next'))
	return resp



def add_self_follows():
	'''Регестрация существующих пользователей как читающих
	самих себя.'''
	for user in User.query.all():
		if not user.is_following(user):
			user.follow(user)
			db.session.add(user)
			db.session.commit()



def check_recaptcha(response, recaptcha_private_key):
	'''Проверка reCaptcha'''
	import urllib, json

	url = 'https://www.google.com/recaptcha/api/siteverify?'
	url = url + 'secret=' +recaptcha_private_key
	url = url + '&response=' +response
	
	try:
		jsonobj = json.loads(urllib.urlopen(url).read())
		if jsonobj['success']:
			return True
		else:
			return False
	except Exception as e:
		print(e)
		return False



def flash_errors(form):
    '''Формирует данные о ошибках в форме'''
    all_errors = [] 
    for field, errors in form.errors.items():
        for error in errors:
            all_errors.append({'field': field, 'error': error})
    return all_errors



def is_moderator(func):
    '''Обёртка для проверки пользователя на авторизацию и является ли
    текущий пользователь модератором.'''
    @wraps(func)
    @login_required
    def wrap(*args, **kwargs):
        if not current_user.is_moderator:
            abort(403)
        return func(*args, **kwargs)
    return wrap


def is_admin(func):
    '''Обёртка для проверки пользователя на авторизацию и является ли
    текущий пользователь администратором.'''
    @wraps(func)
    @login_required
    def wrap(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return func(*args, **kwargs)
    return wrap