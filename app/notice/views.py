#! notice/views.py

#

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import request, current_app

from flask_login import login_required, current_user

from . import notice
from .forms import AddNotice_form
from ..models.notice import Notice
from ..utils import create_response

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@notice.route('/...add')
@login_required
def addNotice_page():
    form = AddNotice_form()
    return create_response(template='notice/add.html', data={
        'page_title': 'Страница создания уведомления',
        'form': form,
    })


@notice.route('/')
@login_required
def notice_page():
    notice = current_user.notice
    count_items = current_app.config['APP_NOTICE_PER_PAGE']

    page = request.args.get('page', default=1, type=int)
    pagination = notice.paginate(page, per_page=count_items, error_out=False)

    return create_response(template='notice/notice.html', data={
        'page_title': 'Страница уведомлений',
        'notice': pagination.items,
        'pagination': pagination,
        'endpoint': 'notice.notice_page',
        'user': current_user
    })