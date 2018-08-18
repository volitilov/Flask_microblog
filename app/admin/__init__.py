# admin package

# инициализирует и получает необходимые данные для работы пакета

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import Blueprint

from .data import page_titles
from ..utils import create_response, is_admin

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

admin = Blueprint(
    name='admin',
    import_name=__name__, 
    static_folder='statics_admin',
    template_folder='templates'
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from .routes import pages, forms_pages, reqs