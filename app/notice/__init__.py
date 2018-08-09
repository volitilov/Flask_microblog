# notice package

# инициализирует и получает необходимые данные для работы пакета

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import Blueprint

from ..models.notice import Notice
from ..models.user import User
from ..models.role import Role
from ..models.post import Post
from ..models.comment import Comment
from .. import db

from .forms import AddNotice_form
from ..utils import create_response

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

notice = Blueprint(
    name='notice', 
    import_name=__name__,
    static_folder='statics_notice',
    template_folder='templates'
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from .routes import pages, forms_pages, reqs