# moderator package

# инициализирует и получает необходимые данные для работы пакета

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import Blueprint

from ..models.post import Post
from ..models.user_settings import UserSettings
from ..models.comment import Comment
from ..models.notice import Notice
from ..models.user import User
from ..models.message import Message
from ..models.tag import Tag, Rel_tag
from ..models.post_rating import Post_rating
from .. import db

from .forms import AddNotice_form
from .data import page_titles, get_data
from ..utils import create_response, flash_errors, is_moderator

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

moderator = Blueprint(
    name='moderator', 
    import_name=__name__
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from .routes import pages, forms_pages, reqs