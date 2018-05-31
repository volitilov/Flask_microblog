# app/api_1_0/coments.py

# - обработка GET-запросов на получения комментариев

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import jsonify, request

from . import api
from ..models.comment import Comment

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@api.route('/comments/')
def get_comments():
    comments = Comment.query.all()
    return jsonify(comments)


@api.route('/comments/<int:id>')
def get_comment(id):
    comment = Comment.query.get_or_404(id)
    return jsonify(comment.to_json())
