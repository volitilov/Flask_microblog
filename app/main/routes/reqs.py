# main/routes/reqs.py

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

