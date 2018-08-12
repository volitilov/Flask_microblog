# post package

# инициализирует и получает необходимые данные для работы пакета

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import Blueprint

from ..models.user import User
from ..models.post import Post
from ..models.comment import Comment
from ..models.tag import Tag, Rel_tag
from ..models.post_rating import Post_rating
from .. import db

from .forms import AddPost_form, EditPost_form
from ..utils import create_response
from .data import get_posts, page_titles

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

post = Blueprint(
    name='post', 
    import_name=__name__,
    static_folder='statics_post',
    template_folder='templates'
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from .routes import pages, forms_pages, reqs