from flask import Blueprint

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

errors = Blueprint(
    name='errors', 
    import_name=__name__, 
    static_folder='statics', 
    template_folder='templates'
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from . import handlers