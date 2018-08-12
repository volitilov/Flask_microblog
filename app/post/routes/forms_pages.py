# post/routes/forms_pages.py

# Обрабатывает страницы с формами

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import flash, current_app, url_for, redirect
from flask_login import current_user, login_required

from .. import (
    # blueprint
    post,

    # utils
    create_response,

    # forms
    AddPost_form, EditPost_form,

    # models
    Post, Tag, Rel_tag,

    # database
    db,

    # data
    get_posts, page_titles
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@post.route(rule='/posts/...add', methods=['GET', 'POST'])
@login_required
def addPost_page():
    '''Генерирует страницу с формай создания постов.'''
    data = get_posts()
    form = AddPost_form()

    if form.validate_on_submit():
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
        return redirect(url_for(endpoint='main.home_page'))

    return create_response(template='add_post.html', data={
        'page_title': page_titles['addPost_page'],
        'form': form,
        'all_posts': data['all_posts'],
        'followed_posts': data['followed_posts']
    })



@post.route(rule='/posts/<int:id>/...edit', methods=['GET', 'POST'])
@login_required
def editPost_page(id):
    '''Генерирует страницу редактирования поста.'''
    data = get_posts()
    form = EditPost_form()
    post = Post.query.get_or_404(id)

    if form.validate_on_submit():
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
        return redirect(url_for('post.editPost_page', id=post.id))
    
    form.text.data = post.text
    form.contents.data = post.table_of_contents

    tags = []
    for rel_tag in post.tags.all():
        tags.append(rel_tag.tag.name)
    form.tags.data = ', '.join(tags)

    return create_response(template='edit_post.html', data={
        'page_title': page_titles['editPost_page'],
        'form': form,
        'post': post,
        'all_posts': data['all_posts'],
        'followed_posts': data['followed_posts']
    })
