# app/api_1_0/users.py

# обработка GET-запросов на получение данных о пользователе, а таже 
# получение данных о написанных или читаемых постах пользователя 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import jsonify

from . import api
from ..models.user import User

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@api.route('/users/<int:id>')
def get_user(id):
    '''Возвращает инфрмацию о запрашиваемом пользователе'''
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())


@api.route('/users/<int:id>/posts/')
def get_userPosts(id):
    '''Возвращает посты написаные пользователем'''
    user = User.query.get_or_404(id)
    posts = [post.to_json() for post in user.posts]
    return jsonify(posts)


@api.route('/users/<int:id>/followed_posts/')
def get_userFollowedPosts(id):
    '''Возвращает посты пользователя на которого подписан запрашиваемый
    пользователь'''
    user = User.query.get_or_404(id)
    followed_posts = [post.to_json() for post in user.followed_posts]
    return jsonify(followed_posts)
