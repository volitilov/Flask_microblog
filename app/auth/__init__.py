# auth package

# инициализирует и получает необходимые данные для работы пакета

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import Blueprint

from ..models.user import User
from ..models.user_settings import UserSettings
from .. import db

from .forms import (
	Login_form, Registration_form, PasswordResetRequest_form, 
	PasswordReset_form
)
from .data import page_titles
from ..email import send_email
from ..utils import create_response

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

auth = Blueprint(
    name='auth', 
    import_name=__name__, 
    static_folder='statics_auth',
    template_folder='templates'
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from .routes import pages, reqs, forms_pages