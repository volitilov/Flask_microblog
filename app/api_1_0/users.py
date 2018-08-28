# app/api_1_0/users.py

# обработка GET-запросов на получение данных о пользователе, а таже 
# получение данных о написанных или читаемых постах пользователя 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import jsonify

from . import (
    # blueprint
    api,

    # errors handler
    not_found,

    # models
    User
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@api.route('/users/<int:id>')
def get_user(id):
    '''Возвращает инфрмацию о запрашиваемом пользователе'''
    user = User.query.get(id)

    if not user:
        return not_found(message='Такого пользователя нет.')

    return jsonify(user.to_json())

