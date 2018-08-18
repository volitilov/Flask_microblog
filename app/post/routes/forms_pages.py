# post/routes/forms_pages.py

# Обрабатывает запросы от форм

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import flash, current_app, url_for, redirect, jsonify
from flask_login import current_user, login_required

from .. import (
    # blueprint
    post,

    # utils
    create_response, flash_errors,

    # forms
    AddPost_form, EditPost_form,

    # models
    Post, Tag, Rel_tag,

    # database
    db
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@post.route(rule='/posts/...add', methods=['POST'])
@login_required
def addPostForm_req():
    '''Обрабатывает отправленные данные формой создания постов.'''
    form = AddPost_form()

    if form.validate():
        title = form.title.data
        contents = form.contents.data
        text = form.text.data

        post = Post(title=title, table_of_contents=contents, text=text, 
            author=current_user)
        
        all_tags = []
        rel_tags = []
        form_tags = form.tags.data.split(',')
        for tag in form_tags:
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

        flash(message='Пост отправлен на модерацию')
        return jsonify({'next_url': url_for(endpoint='main.home_page')})

    return jsonify({'errors': flash_errors(form)})



@post.route(rule='/posts/<int:id>/...edit', methods=['POST'])
@login_required
def editPostForm_req(id):
    '''Обрабатывает отправленные данные формой редактирования 
    поста.'''
    form = EditPost_form()
    post = Post.query.get_or_404(id)

    if current_user != post.author:
        flash(category='warn', message='Вы не являетесь автором публикации.')
        return redirect(url_for('post.posts_page'))

    if post.state == 'moderation':
        return redirect(url_for('post.post_page', id=post.id))

    if form.validate():
        post.tags.delete()
        post.title = form.title.data
        post.text = form.text.data
        post.table_of_contents = form.contents.data
        post.state = 'moderation'

        all_tags = []
        rel_tags = []
        form_tags = form.tags.data.split(',')
        for tag in form_tags:
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

        flash(message='Пост отправлен на модерацию.')
        return jsonify({'next_url': url_for('post.userPosts_page', username=current_user.name)})
    
    return jsonify({'errors': flash_errors(form)})
