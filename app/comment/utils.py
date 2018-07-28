# comment/utils.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from functools import wraps

from flask_login import current_user

from ..models.comment import Comment
from ..utils import create_response


# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

create_response = create_response
