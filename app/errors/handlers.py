# app/errors/errors.py

#

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import request, jsonify

from . import errors
from ..utils import create_response

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@errors.app_errorhandler(403)
def forbidden(message):
    if request.accept_mimetypes.accept_json and \
        not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'forbidden', 'message': message})
        response.status_code = 403
        return response
    return create_response(template='403.html', data={
		'page_title': '403 страница'
	}), 403



@errors.app_errorhandler(404)
def page_not_found(e):
	if request.accept_mimetypes.accept_json and \
		not request.accept_mimetypes.accept_html:
		response = jsonify({'error': 'not found'})
		response.status_code = 404
		return response
	return create_response(template='404.html', data={
		'page_title': '404 страница'
	}), 404



@errors.app_errorhandler(500)
def internal_server_error(e):
	if request.accept_mimetypes.accept_json and \
		not request.accept_mimetypes.accept_html:
		response = jsonify({'error': 'internal server error'})
		response.status_code = 500
		return response
	return create_response(template='500.html', data={
		'page_title': '500 страница'
	}), 500

