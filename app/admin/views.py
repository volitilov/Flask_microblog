# admin/views.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import (
	render_template, redirect, request, url_for, flash, session
)

# flask extensions
from flask_login import current_user, login_required

# app modules
from . import admin
from ..utils import create_response

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@admin.route('/admin')
@login_required
def admin_page():
    if not current_user.is_admin():
        flash(category='warn', message='Тебе туда нельзя')
        return redirect(url_for('main.home_page'))
    else:
        return render_template('admin/panell.html', data={
            'title_page': 'Страница администратора.'
        })
