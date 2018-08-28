# app/api_1_0/posts.py

# - обработка GET-запросов на получения постов
# - обработка POST-запросов добавляющих новые посты
# - обработка GET-запросов на получение постов пользователя 
# - обработка GET-запросов на постов читаемых пользователем

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import jsonify, request, url_for, current_app, g

from . import (
    # blueprint
    api,

    # error handler
    forbidden,

    # database
    db,

    # models
    Post, Comment, User, Tag, Rel_tag
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@api.route('/posts/')
def get_posts():
    '''Возвращает все посты'''
    page = request.args.get('page', 1, type=int)
    count_items = current_app.config['APP_POSTS_PER_PAGE']
    posts = Post.query.filter_by(state='public')

    pagination = posts.paginate(
        page, per_page=count_items, error_out=False)
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
    '''Возвращает запрошеный пост по id.'''
    post = Post.query.get_or_404(id)

    if post.state == 'moderation':
        return jsonify({'message': 'Пост находится на модерации.'})
    
    return jsonify(post.to_json())



@api.route('/posts/', methods=['POST'])
def new_post():
    '''Выполняет публикацию поста и возвращает опубликованый пост, 
    а также абсолютный адрес к данному посту'''
    if not g.current_user.writer:
        return forbidden(
            'Вы не можете добавлять публикации, т.к. не являетесь автором.')

    post = Post.from_json(request.json)
    post.author = g.current_user

    all_tags = []
    rel_tags = []
    req_tags = request.json.get('tags').split(',')
    for tag in req_tags:
        tag_name = tag.strip(' ')
        tag = Tag.query.filter_by(name=tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
        
        rel_tag = Rel_tag.query.filter_by(post=post, tag=tag).first()
        if not rel_tag:
            rel_tag = Rel_tag(post=post, tag=tag)

        all_tags.append(tag)
        rel_tags.append(rel_tag)

    db.session.add(post)
    db.session.add_all(all_tags)
    db.session.add_all(rel_tags)
    db.session.commit()

    return jsonify({'message': 'Пост отправлен на модерацию.'}), 201



@api.route('/posts/<int:id>', methods=['PUT'])
def edit_post(id):
    '''Выполняет запрос на редактирование поста и в случае успеха
    возвращает отредактироаный пост.'''
    post = Post.query.get_or_404(id)
    
    if g.current_user != post.author:
        return forbidden('Вы не можете редактировать данный пост.')

    if post.state == 'moderation':
        return forbidden('На данный момент вы не можите редактировать пост.')
    
    post.title = request.json.get('title', post.title)
    post.table_of_contents = request.json.get('table_of_contents', post.table_of_contents)
    post.text = request.json.get('body', post.text)
    post.state = 'moderation'

    if request.json.get('tags'):
        all_tags = []
        rel_tags = []
        req_tags = request.json.get('tags').split(',')
        for tag in req_tags:
            tag_name = tag.strip(' ')
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
            
            rel_tag = Rel_tag.query.filter_by(post=post, tag=tag).first()
            if not rel_tag:
                rel_tag = Rel_tag(post=post, tag=tag)

            all_tags.append(tag)
            rel_tags.append(rel_tag)

        db.session.add_all(all_tags)
        db.session.add_all(rel_tags)

    db.session.add(post)
    db.session.commit()

    return jsonify({'message': 'Пост отправлен на модерацию.'}), 201



@api.route('/users/<int:id>/posts/')
def get_userPosts(id):
    '''Возвращает посты написаные пользователем'''
    user = User.query.get(id)
    if not user:
        return not_found(message='Такого пользователя нет.')
    
    posts = user.posts.filter_by(state='public')
    posts = [post.to_json() for post in posts]
    return jsonify(posts)



@api.route('/users/<int:id>/followed_posts/')
def get_userFollowedPosts(id):
    '''Возвращает посты пользователя на которого подписан запрашиваемый
    пользователь'''
    user = User.query.get(id)
    if not user:
        return not_found(message='Такого пользователя нет.')
        
    followed_posts = user.followed_posts.filter(Post.state=='public')
    followed_posts = [post.to_json() for post in followed_posts]
    return jsonify(followed_posts)
