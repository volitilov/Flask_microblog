# app/api_1_0/coments.py

# - обработка GET-запросов на получения комментариев

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import jsonify, request

from . import api
from ..models.comment import Comment

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@api.route('/comments/')
def get_comments():
    '''Возвращает все комментарии'''
    comments = Comment.query.all()
    return jsonify([comment.to_json() for comment in comments])


@api.route('/comments/<int:id>')
def get_comment(id):
    '''Возвращает запрашиваемый комментарий'''
    comment = Comment.query.get_or_404(id)
    return jsonify(comment.to_json())
