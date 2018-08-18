# admin/routes/pages.py

# Обрабатывает GET-запросы
# Формирует страницы для запрошенных урлов 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import redirect, url_for, flash
from flask_login import current_user, login_required

from .. import (
    # blueprint
    admin, 
    
    # utils
    create_response, is_admin,

    # data
    page_titles
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@admin.route('/admin')
@is_admin
def dashboard_page():
    return create_response(template='dashboard.html', data={
        'title_page': page_titles['dashboard_page']
    })

