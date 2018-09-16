# admin/routes/pages.py

# Обрабатывает GET-запросы
# Формирует страницы для запрошенных урлов 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import redirect, url_for, flash, current_app, request
from flask_login import current_user, login_required

from .. import (
    # blueprint
    admin,

    # models
    User, Role, Notice, Post, Comment, Tag,
    
    # utils
    create_response, is_admin,

    # data
    page_titles
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@admin.route('/')
@is_admin
def dashboard_page():
    return create_response(template='admin/dashboard.html', data={
        'page': 'dashboard',
        'title_page': page_titles['dashboard_page']
    })


@admin.route('/roles')
@is_admin
def adminRoles_page():
    roles = Role.query.all()
    return create_response(template='admin/adminRoles.html', data={
        'page': 'roles',
        'roles': roles,
        'title_page': page_titles['adminRoles_page']
    })


@admin.route('/roles/<role>/users')
@is_admin
def adminRoleUsers_page(role):
    role = Role.query.filter_by(name=role).first()
    return create_response(template='admin/adminRoleUsers.html', data={
        'users': role.users,
        'title_page': page_titles['adminRoleUsers_page']
    })


@admin.route('/notice')
@is_admin
def adminNotice_page():
    notice = Notice.query.filter_by(author=current_user)
    count_items = current_app.config['ADMIN_NOTICE_PER_PAGE']

    page = request.args.get('page', 1, type=int)
    pagination = notice.paginate(
        page, per_page=count_items, error_out=False)

    return create_response(template='admin/adminNotice.html', data={
        'page': 'notice',
        'all_notice': notice,
        'pagination': pagination,
        'page_notice': pagination.items,
        'endpoint': 'admin.adminNotice_page',
        'title_page': page_titles['adminNotice_page'],
        'count_items': count_items
    })


@admin.route('/users')
@is_admin
def adminUsers_page():
    users = User.query
    count_items = current_app.config['ADMIN_USERS_PER_PAGE']

    page = request.args.get('page', 1, type=int)
    pagination = users.paginate(
        page, per_page=count_items, error_out=False)

    return create_response(template='admin/adminUsers.html', data={
        'page': 'users',
        'all_users': users,
        'pagination': pagination,
        'page_users': pagination.items,
        'endpoint': 'admin.adminUsers_page',
        'title_page': page_titles['adminUsers_page'],
        'count_items': count_items
    })


@admin.route('/posts')
@is_admin
def adminPosts_page():
    posts = Post.query
    count_items = current_app.config['ADMIN_POSTS_PER_PAGE']

    page = request.args.get('page', 1, type=int)
    pagination = posts.paginate(
        page, per_page=count_items, error_out=False)

    return create_response(template='admin/adminPosts.html', data={
        'page': 'posts',
        'all_posts': posts,
        'pagination': pagination,
        'page_posts': pagination.items,
        'endpoint': 'admin.adminPosts_page',
        'title_page': page_titles['adminPosts_page'],
        'count_items': count_items
    })


@admin.route('/comments')
@is_admin
def adminComments_page():
    comments = Comment.query
    count_items = current_app.config['ADMIN_COMMENTS_PER_PAGE']

    page = request.args.get('page', 1, type=int)
    pagination = comments.paginate(
        page, per_page=count_items, error_out=False)

    return create_response(template='admin/adminComments.html', data={
        'page': 'comments',
        'all_comments': comments,
        'pagination': pagination,
        'page_comments': pagination.items,
        'endpoint': 'admin.adminComments_page',
        'title_page': page_titles['adminComments_page'],
        'count_items': count_items
    })


@admin.route('/tags')
@is_admin
def adminTags_page():
    tags = Tag.query
    count_items = current_app.config['ADMIN_TAGS_PER_PAGE']

    page = request.args.get('page', 1, type=int)
    pagination = tags.paginate(
        page, per_page=count_items, error_out=False)

    return create_response(template='admin/adminTags.html', data={
        'page': 'tags',
        'all_tags': tags,
        'pagination': pagination,
        'page_tags': pagination.items,
        'endpoint': 'admin.adminTags_page',
        'title_page': page_titles['adminTags_page'],
        'count_items': count_items
    })