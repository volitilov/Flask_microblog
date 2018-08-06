from flask import Blueprint

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

errors = Blueprint(
    name='errors', 
    import_name=__name__, 
    static_folder='statics_errors', 
    template_folder='templates'
)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from . import handlers