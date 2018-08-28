# errors/errors.py

#

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import request, jsonify, render_template

from . import (
    # blueprint
    errors,

    # forms
    Search_form,

    # data
    page_titles,

    # utils
    create_response
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@errors.app_errorhandler(404)
def page_not_found(e):
    '''Генерирует и обрабатывает 404 ошибку'''
    form = Search_form()
    
    print(request.accept_mimetypes.accept_json)
    print(request.accept_mimetypes.accept_html)

    if request.accept_mimetypes.accept_json and \
        not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response

    return create_response(template='404.html', data={
        'page_title': page_titles['page_not_found'],
        'form': form
    }), 404



@errors.app_errorhandler(500)
def internal_server_error(e):
    '''Генерирует и обрабатывает 500 ошибку.'''
    if request.accept_mimetypes.accept_json and \
        not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'internal server error'})
        response.status_code = 500
        return response
    return create_response(template='500.html', data={
        'page_title': page_titles['internal_server_error']
    }), 500

