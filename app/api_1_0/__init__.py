# api package

# инициализирует и получает необходимые данные для работы api

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import Blueprint

api = Blueprint('api', __name__)

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from ..models.user import User
from ..models.comment import Comment
from ..models.post import Post
from ..models.tag import Tag, Rel_tag
from .. import db

from .errors import unauthorized, forbidden, not_found

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from . import authentication, posts, users, comments, errors
