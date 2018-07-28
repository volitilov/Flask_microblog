#! notice/views.py

#

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import request, current_app, flash, redirect, url_for

from flask_login import login_required, current_user

from . import notice
from .forms import AddNotice_form
from ..models.notice import Notice
from ..models.post import Post
from ..models.comment import Comment
from ..utils import create_response

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@notice.route('/<username>/notice/add')
@login_required
def addNotice_page(username):
    form = AddNotice_form()
    return create_response(template='notice/add.html', data={
        'page_title': 'Страница создания уведомления',
        'form': form,
    })


@notice.route('/<username>/notice')
@login_required
def notice_page(username):
    if current_user.name != username:
        flash(category='warn', 
            message='У вас есть доступ, только к своим уведомлениям')
        return redirect(url_for('notice.notice_page', username=current_user.name))

    posts = current_user.posts.filter(Post.state!='moderator')
    comments = current_user.comments.filter(Comment.state!='moderation')
    notice = current_user.notice
    count_items = current_app.config['APP_NOTICE_PER_PAGE']

    page = request.args.get('page', default=1, type=int)
    pagination = notice.order_by(Notice.timestamp.desc()).paginate(
        page, per_page=count_items, error_out=False)

    return create_response(template='notice/notice.html', data={
        'page_title': 'Страница уведомлений',
        'notice': pagination.items,
        'posts': posts,
        'comments': comments,
        'pagination': pagination,
        'endpoint': 'notice.notice_page',
        'user': current_user,
        'notice_count': notice.count(),
        'notice_per_page': count_items
    })

