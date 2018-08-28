# auth/routes/pages.py

# Обрабатывает GET-запросы
# Формирует страницы для запрошенных урлов 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import redirect, url_for
from flask_login import current_user

from .. import (
	# blueprint
	auth,

	# utils
	create_response,

	# forms
	Login_form, Registration_form, PasswordResetRequest_form,
	PasswordReset_form,

	# data
	page_titles
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@auth.route(rule='/unconfirmed')
def unconfirmed_page():
	'''Генерирует страницу с предложением потвердить свою учетную запись'''
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for('main.home_page'))
	return create_response(template='unconfirmed.html', data={
		'page_title': page_titles['unconfirmed_page']
	})


@auth.route(rule='/login')
def login_page():
    '''Генерирует страницу авторизации'''
    if not current_user.is_anonymous:
        return redirect(url_for('main.home_page'))
        
    form = Login_form()
    return create_response(template='login.html', data={
        'form': form,
        'page_title': page_titles['login_page']
    })



@auth.route(rule='/register')
def registration_page():
    '''Генерирует страницу регистрации'''
    form = Registration_form()
    return create_response(template='registr.html', data={
        'form': form,
        'page_title': page_titles['registration_page']
    })



@auth.route(rule='/reset_password')
def resetPassword_page():
    '''Генерирует страницу запроса для сброса пароля'''
    form = PasswordResetRequest_form()
    return create_response(template='reset_password_request.html', data={
        'page_title': page_titles['resetPassword_page'],
        'form': form
    })



@auth.route(rule='/reset/<token>')
def passwordReset_page(token):
    '''Обрабатывает запрос на изменения пароля'''
    form = PasswordReset_form()
    return create_response(template='reset_password.html', data={
        'page_title': page_titles['passwordReset_page'],
        'form': form,
		'token': token
    })



