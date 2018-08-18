# comment package

# инициализирует и получает необходимые данные для работы пакета

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import Blueprint

from ..models.post import Post
from ..models.user import User
from ..models.comment import Comment
from ..models.notice import Notice
from ..models.user_settings import UserSettings
from .. import db

from ..utils import create_response, flash_errors
from .data import page_titles, get_data
from .forms import AddComment_form

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

comment = Blueprint(
    name='comment', 
    import_name=__name__, 
    static_folder='statics_comments',
    template_folder='templates'
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from .routes import pages, reqs, forms_pages