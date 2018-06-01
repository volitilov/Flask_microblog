# app/api_1_0/posts.py

# - обработка GET-запросов на получения постов
# - обработка POST-запросов добавляющих новые посты
# - обработка GET-запросов на получение комментариев запрашиваемого поста
# - обработка POST-запросов на добавления комментария к посту

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import jsonify, request, url_for, current_app, g

from . import api
from .errors import forbidden
from .. import db
from ..models.post import Post
from ..models.comment import Comment

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@api.route('/posts/')
def get_posts():
    '''Возвращает все посты'''
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_posts', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_posts', page=page+1, _external=True)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/posts/<int:id>')
def get_post(id):
    '''Возвращает запрошеный пост по id'''
    post = Post.query.get_or_404(id)
    return jsonify(post.to_json())


@api.route('/posts/', methods=['POST'])
def new_post():
    '''Выполняет публикацию поста и возвращает опубликованый пост, 
    а также абсолютный адрес к данному посту'''
    post = Post.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json()), 201, \
        {'Location': url_for('api.get_post', id=post.id, _external=True)}


@api.route('/posts/<int:id>', methods=['PUT'])
def edit_post(id):
    '''Выполняет запрос на редактирование поста и в случае успеха
    возвращает отредактироаный пост.'''
    post = Post.query.get_or_404(id)
    if g.current_user != post.author:
        return forbidden('Insufficient permissions')
    post.body = request.json.get('body', post.text)
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json())


@api.route('/posts/<int:id>/comments/')
def get_postComments(id):
    '''Возвращает комметарии запрашиваемого поста'''
    post = Post.query.get_or_404(id)
    comments = [comment.to_json() for comment in post.comments]
    return jsonify(comments)


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
