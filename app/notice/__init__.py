from flask import Blueprint

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

notice = Blueprint('notice', __name__, url_prefix='/notice')

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from . import views, req