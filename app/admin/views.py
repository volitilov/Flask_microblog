# admin/views.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import (
	render_template, redirect, request, url_for, flash, session
)

# flask extensions
from flask_login import current_user, login_user

# app modules
from . import admin
from ..models import User, Post, Role
from ..email import send_email
from .. import db

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@admin.route('/admin')
def adminLogin_page():
    data = {
        'title_page': 'Страница администратора.'
    }

    if current_user.is_anonymous:
        return redirect(url_for('auth.login_page'))

    if current_user.is_admin():
        return render_template('admin/panell.html', data=data)
    else:
        flash('Тебе туда нельзя')
        return redirect(url_for('main.home_page'))
