# main package

# инициализирует и получает необходимые данные для работы пакета

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import Blueprint

from ..models.post import Post
from ..models.tag import Tag
from ..models.user import User
from ..models.message import Message
from .. import db

from .forms import Search_form, Support_form
from .data import page_titles
from ..utils import create_response, flash_errors

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

main = Blueprint(
    name='main', 
    import_name=__name__, 
    static_folder='statics_main',
    template_folder='templates'
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from .routes import pages, forms_pages, reqs