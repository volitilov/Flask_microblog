# notice/routes/pages.py

# Обрабатывает GET-запросы
# Формирует страницы для запрошенных урлов 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import request, current_app, flash, redirect, url_for
from flask_login import login_required, current_user

from .. import (
    # blueprint
    notice,

    # models
    Notice, Post, Comment,

    # forms
    AddNotice_form,

    # utils
    create_response, is_admin,

    # data
    page_titles
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@notice.route('/notice')
@login_required
def notice_page():
    posts = current_user.posts.filter(Post.state!='moderator')
    comments = current_user.comments.filter(Comment.state!='moderation')
    notice = current_user.notice
    count_items = current_app.config['APP_NOTICE_PER_PAGE']

    page = request.args.get('page', default=1, type=int)
    pagination = notice.order_by(Notice.timestamp.desc()).paginate(
        page, per_page=count_items, error_out=False)

    return create_response(template='notice.html', data={
        'page_title': page_titles['notice_page'],
        'notice': pagination.items,
        'posts': posts,
        'comments': comments,
        'pagination': pagination,
        'endpoint': 'notice.notice_page',
        'user': current_user,
        'notice_count': notice.count(),
        'notice_per_page': count_items
    })



@notice.route('/notice/add')
@is_admin
def addNotice_page():
    form = AddNotice_form()

    return create_response(template='add_notice.html', data={
        'page_title': page_titles['addNotice_page'],
        'form': form,
    })