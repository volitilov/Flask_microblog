# post/req.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import redirect, request, url_for, flash, current_app

from flask_login import current_user, login_required

from . import main
from .forms import Search_form
from ..models.post import Post
from .. import db

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@main.route('/posts/...search')
def search_request():
    form = Search_form()

    if not form.validate():
        return redirect(url_for('main.home_page'))
    
    return redirect(url_for('main.searchResults_page', data=form.q.data))