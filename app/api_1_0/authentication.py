# app/api_1_0/authentication.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import g, jsonify, request
from flask_httpauth import HTTPBasicAuth

from . import api
from .errors import unauthorized, forbidden
from ..models.user import User

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

auth = HTTPBasicAuth()

@api.before_request
@auth.login_required
def before_request():
    '''Провека пользователя'''
    if g.current_user.is_anonymous: 
        return forbidden(message='Доступ анонимным пользователям воспрещён')

    if not g.current_user.confirmed:
        return forbidden('Аккаунт не подтверждён')



@auth.verify_password
def verify_password(email_or_token, password):
    '''Проверка авторизации'''
    if email_or_token == '':
        return False
    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(email=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)



@api.route('/token')
def get_token():
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized(message='Invalid credentials')

    token = g.current_user.generate_auth_token(expiration=3600)
    return jsonify({
        'token': token.decode(encoding='utf-8'),
        'expiration': 3600
    })



@auth.error_handler
def auth_error():
    return unauthorized(message='Неверные учётные данные')


