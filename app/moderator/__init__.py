from flask import Blueprint

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

moderator = Blueprint('moderator', __name__, url_prefix='/moderator')

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from . import views, req