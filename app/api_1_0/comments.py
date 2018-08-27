# app/api_1_0/coments.py

# - обработка GET-запросов на получения комментариев
# - обработка POST-запросов на добавления комментария к посту
# - обработка GET-запросов на получение комментариев запрашиваемого поста

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import jsonify, request, g

from . import api
from .errors import forbidden, not_found
from ..models.comment import Comment
from ..models.post import Post
from .. import db

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@api.route('/comments/')
def get_allComments():
    '''Возвращает все комментарии'''
    comments = Comment.query.filter_by(state='public').all()
    return jsonify([comment.to_json() for comment in comments])



@api.route('/comments/<int:id>')
def get_comment(id):
    '''Возвращает запрашиваемый комментарий'''
    comment = Comment.query.get(id)
    if not comment:
        return not_found('Такого комментария нет.')
        
    if comment.state == 'moderation':
        return jsonify({'message': 'Комментарий находится на модерации.'})
    
    return jsonify(comment.to_json())



@api.route('/posts/<int:id>/comments/', methods=['POST'])
def add_comment(id):
    '''Выполняет запрос на добавление комментария и возвращает
    опублекованный комментарий и его абсолютный адрес'''
    post = Post.query.get(id)
    if not post:
        return not_found(message='Пост к которому вы запрашиваете комментарии, отсутствует.')
    comment = Comment.from_json(request.json)
    
    comment.post = post
    comment.author = g.current_user
    comment.state = 'moderation'
    db.session.add(comment)
    db.session.commit()

    return jsonify({'message': 'Комментарий отправлен на модерацию.'}), 201



@api.route('/comments/<int:id>', methods=['PUT'])
def edit_Comment(id):
    '''Выполняет редактирование комментария.'''
    comment = Comment.query.get(id)

    if not comment:
        return not_found('Такого комментария нет.')

    if comment.author != g.current_user:
        return forbidden('Вы не можете редактировать данный комментарий.')

    if comment.state == 'moderation':
        return forbidden('Комментарий находится на модерации.')

    comment.body = request.json.get('body', comment.body)
    comment.state = 'moderation'
    db.session.add(comment)
    db.session.commit()
    
    return jsonify({'message': 'Комментарий отправлен на модерацию'}), 201



@api.route('/posts/<int:id>/comments/')
def get_postComments(id):
    '''Возвращает комметарии запрашиваемого поста'''
    post = Post.query.get(id)
    if not post:
        return not_found(message='Пост к которому вы запрашиваете комментарии, отсутствует.')
    comments = post.comments.filter_by(state='public')
    comments = [comment.to_json() for comment in comments]
    return jsonify(comments)
