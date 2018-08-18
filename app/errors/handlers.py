# errors/errors.py

#

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import request, jsonify

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

@errors.app_errorhandler(403)
def forbidden(message):
    '''Генерирует и обрабатывает 403 ошибку.'''
    if request.accept_mimetypes.accept_json and \
        not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'forbidden', 'message': message})
        response.status_code = 403
        return response
    return create_response(template='403.html', data={
        'page_title': page_titles['forbidden']
    }), 403



@errors.app_errorhandler(404)
def page_not_found(e):
    '''Генерирует и обрабатывает 404 ошибку'''
    form = Search_form()
    
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

