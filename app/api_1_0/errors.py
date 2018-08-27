# app/api_1_0/errors.py

#

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import request, jsonify
from app.exceptions import ValidationError

from . import api

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

def bad_request(message):
    '''Возвращает ошибку запроса.'''
    response = jsonify({'error': 'bad_request', 'message': message})
    response.status_code = 400
    return response


def unauthorized(message):
    '''Возвращает ошибку авторизации.'''
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


def forbidden(message):
    ''''''
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


def method_not_allowed(message):
    '''Возвращает ошибку неподдерживаемого метода.'''
    response = jsonify({'error': 'method_not_allowed', 'message': message})
    response.status_code = 405
    return response


@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])