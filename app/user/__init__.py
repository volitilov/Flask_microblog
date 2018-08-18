# user package

# инициализирует и получает необходимые данные для работы пакета

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import Blueprint

from ..models.user import User
from ..models.post import Post
from ..models.notice import Notice
from ..models.comment import Comment
from ..models.user_settings import UserSettings
from .. import db

from ..utils import create_response, flash_errors
from ..email import send_email

from .utils import FileSize
from .forms import (
    EditProfile_form, ChangeEmail_form, ChangeLogin_form, 
    ChangePassword_form, EditNotice_form, AddNotice_form
)
from .data import page_titles

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

user = Blueprint(
    name='user', 
    import_name=__name__,
    static_folder='statics_user',
    template_folder='templates'
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from .routes import pages, forms_pages, reqs