# app/utils.py

#

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import make_response, render_template, request

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

def create_response(template, data):
	resp = make_response(render_template(template, data=data))
	# resp.set_cookie(key='previous', value=request.full_path)
	if request.args.get('next') is not None: 
		resp.set_cookie(key='next', value=request.args.get('next'))
	return resp