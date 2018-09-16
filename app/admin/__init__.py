# admin package

# инициализирует и получает необходимые данные для работы пакета

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import Blueprint

from ..models.role import Role
from ..models.user import User
from ..models.notice import Notice
from ..models.post import Post
from ..models.comment import Comment
from ..models.tag import Tag
from .data import page_titles

from ..utils import create_response, is_admin

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

admin = Blueprint(
    name='admin',
    import_name=__name__,
    url_prefix='/admin'
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from .routes import pages, forms_pages, reqs