# moderator/req.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from flask import redirect, request, url_for, flash, current_app

from flask_login import current_user, login_required

from . import moderator
from .utils import is_moderator
from ..models.post import Post
from ..models.tag import Tag, Rel_tag
from ..models.post_rating import Post_rating
from .. import db

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@moderator.route('/posts/<int:id>...confirm')
@is_moderator
def confirmPost_request(id):
    post = Post.query.get(id)
    post.moderation = True
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('moderator.posts_page'))


@moderator.route('/posts/<int:id>...del')
@is_moderator
def deletePost_request(id):
	post = Post.query.get(id)

	db.session.delete(post)
	db.session.commit()

	flash(message='Пост успешно удалён', category='success')
	return redirect(url_for('moderator.posts_page'))