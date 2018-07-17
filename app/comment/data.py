# comment/data.py

# 

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from ..models.post import Post
from ..models.comment import Comment

# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

def get_data(current_user, user):
    if current_user == user:
        return {
            'posts': user.posts.filter(Post.state!='moderation'),
            'comments': user.comments.filter(Comment.state!='moderation')
        }
    else:
        return {
            'posts': user.posts.filter_by(state='public'),
            'comments': user.comments.filter_by(state='public')
        }



page_titles = {
    'addComment_page': 'Страница добавления комментария',
    'comments_page': 'Страница с комментариями пользователя.',
    'comment_page': 'Страница комментария',
    'editComment_page': 'Страница редактирования коментария'
}