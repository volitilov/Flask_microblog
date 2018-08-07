# main/routes/req.py

# Обрабатывает POST-запросы 
# Работа с данными: добавление, редактирование, удаление

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import redirect, url_for, current_app

from flask_sqlalchemy import get_debug_queries

from .. import (
    # blueprint
    main,

    # forms 
    Search_form, 
    
    # models 
    Post,

    # database
    db
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@main.after_app_request
def after_request(response):
    '''Ведёт отчёт в виде списка о медлиных запросов к базе данных'''
    for query in get_debug_queries():
        if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration,
                query.context))
    return response



@main.route('/posts/...search')
def search_request():
    form = Search_form()

    if not form.validate():
        return redirect(url_for('main.home_page'))
    
    return redirect(url_for('main.searchResults_page', data=form.q.data))