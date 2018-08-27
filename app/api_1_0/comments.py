# app/api_1_0/coments.py

# - обработка GET-запросов на получения комментариев
# - обработка POST-запросов на добавления комментария к посту
# - обработка GET-запросов на получение комментариев запрашиваемого поста

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import jsonify, request, g

from . import api
from ..models.comment import Comment
from ..models.post import Post
from .. import db

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



@api.route('/posts/<int:id>/comments/', methods=['POST'])
def add_postComment(id):
    '''Выполняет запрос на добавление комментария и возвращает
    опублекованный комментарий и его абсолютный адрес'''
    post = Post.query.get_or_404(id)
    if request.method == 'POST':
        comment = Comment.from_json(request.json)
        comment.post = post
        comment.author = g.current_user
        db.session.add(comment)
        db.session.commit()

    return jsonify(comment.to_json()), 201, \
        {'Location': url_for('api.get_comment', id=comment.id, _external=True)}



@api.route('/posts/<int:id>/comments/')
def get_postComments(id):
    '''Возвращает комметарии запрашиваемого поста'''
    post = Post.query.get_or_404(id)
    comments = [comment.to_json() for comment in post.comments]
    return jsonify(comments)
