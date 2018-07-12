# post/utils.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from functools import wraps

from flask_login import current_user

from ..models.post import Post
from ..utils import create_response


# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

create_response = create_response
