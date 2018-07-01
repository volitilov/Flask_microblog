#! notice/views.py

#

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import request, current_app

from flask_login import login_required, current_user

from . import notice
from .forms import AddNotice_form, SettingsNotice_form
from ..models.notice import Notice
from ..models.user_settings import UserSettings
from ..utils import create_response

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@notice.route('/add')
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
    pagination = notice.order_by(Notice.timestamp.desc()).paginate(
        page, per_page=count_items, error_out=False)

    return create_response(template='notice/notice.html', data={
        'page_title': 'Страница уведомлений',
        'notice': pagination.items,
        'pagination': pagination,
        'endpoint': 'notice.notice_page',
        'user': current_user,
        'notice_count': notice.count(),
        'notice_per_page': count_items
    })



@notice.route('/settings')
@login_required
def noticeSettings_page():
    form = SettingsNotice_form()
    user_settings = UserSettings.query.filter_by(state='custom', profile=current_user).first()

    form.comments_me.data = user_settings.comments_me
    form.follow_me.data = user_settings.follow_me
    form.unfollow_me.data = user_settings.unfollow_me
    form.unsubscribe_me.data = user_settings.unsubscribe_me
    form.comment_moderated.data = user_settings.comment_moderated
    form.post_moderated.data = user_settings.post_moderated

    return create_response(template='notice/settings.html', data={
        'page_title': 'Страница настроек уведомлений',
        'page': 'notice_settings',
        'form': form
    })