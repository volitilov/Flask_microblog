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
    create_response,

    # data
    page_titles
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@admin.route('/admin')
@login_required
def dashboard_page():
    if not current_user.is_admin():
        flash(category='warn', message='Тебе туда нельзя')
        return redirect(url_for('main.home_page'))
    else:
        return create_response(template='dashboard.html', data={
            'title_page': page_titles['dashboard_page']
        })

