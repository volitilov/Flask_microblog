# errors package

# инициализирует и получает необходимые данные для работы пакета

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import Blueprint

from .forms import Search_form
from .data import page_titles
from ..utils import create_response, flash_errors

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

errors = Blueprint(
    name='errors', 
    import_name=__name__
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from . import handlers